from dataclasses import asdict, dataclass, field, InitVar
import logging
import os
from unittest import mock

import google.auth.credentials
from google.cloud.firestore import Client

from ..clients import retry
from ..exceptions import TransientException
from ..settings import RBX_PROJECT

logger = logging.getLogger("rbx.auth")


class Keystore:
    """Manages API Keys stored in Google Cloud Firestore (Native Mode)."""

    def __init__(self):
        if os.getenv("GAE_ENV", "").startswith("standard"):
            db = Client(project=RBX_PROJECT)
        else:
            credentials = mock.Mock(spec=google.auth.credentials.Credentials)
            db = Client(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"), credentials=credentials
            )

        self.collection = db.collection("api_keys")
        self.inventory = db.collection("inventory")

    def _inventory(self, key, document):
        """Given a DocumentSnapshot, return the fully loaded Inventory object."""
        return Inventory(**{"key": key, "keystore": self, **document.to_dict()})

    def _key(self, document):
        """Given a DocumentSnapshot, return the fully loaded Key object."""
        return Key(**{"keystore": self, "key_id": document.id, **document.to_dict()})

    def add_campaign(self, campaign):
        """Add a campaign to the campaigns inventory."""
        self.add_campaigns([campaign])

    @retry.Retry(deadline=300.0)
    def add_campaigns(self, campaigns):
        """Add campaigns to the campaigns inventory."""
        inventory = self.get_inventory()
        inventory.add(campaigns)

    @retry.Retry(deadline=300.0)
    def create_key(
        self, email, name, campaigns=None, is_restricted=None, services=None
    ):
        """Make a new API key.

        A key is associated with a user via her email address. If a key already exists for that
        user, the key is updated instead.
        """
        key = self.get_key(email=email)
        if not key:
            key = {
                "campaigns": campaigns or [],
                "email": email,
                "is_restricted": is_restricted if is_restricted is not None else True,
                "name": name,
                "services": services if services is not None else ["*.*"],
                "status": "active",
            }

            _, ref = self.collection.add(key)
            if not ref.get().exists:
                raise TransientException(f"Failed to create key for {email}")

            key = self._key(ref.get())
        else:
            key.update(
                **{
                    "campaigns": campaigns or key.campaigns,
                    "is_restricted": is_restricted
                    if is_restricted is not None
                    else key.is_restricted,
                    "name": name or key.name,
                    "services": services or key.services,
                    "status": "active",  # the key is resuscitated
                }
            )

        # Unrestricted keys get access to all inventory
        if not key.is_restricted:
            key.campaigns = self.get_campaigns()

        return key

    def get_campaigns(self):
        """List all campaigns in the inventory."""
        inventory = self.get_inventory()
        if not inventory:
            return []

        return inventory.values

    def get_inventory(self, key="campaigns"):
        """Retrieve a key from the inventory."""
        document = self.inventory.document(key).get()
        if not document.exists:
            return Inventory(key=key, keystore=self)
        else:
            return self._inventory(key, document)

    def get_key(self, key_id=None, email=None):
        """Retrieve a key by ID or email."""
        key = None

        if key_id:
            document = self.collection.document(key_id).get()
            if document.exists:
                key = self._key(document)

        if email:
            document = next(self.collection.where("email", "==", email).stream(), False)
            if document:
                key = self._key(document)

        # Unrestricted keys get access to all inventory
        if key and not key.is_restricted:
            key.campaigns = self.get_campaigns()

        return key

    def update_key(self, key, attributes):
        """Set the new Key values in Firestore."""
        assert isinstance(key, Key), f"excepted rbx.auth.Key, got {type(key)}"
        document = self.collection.document(key.key_id)
        document.set(attributes, merge=True)


@dataclass
class Inventory:
    key: InitVar[str]
    keystore: InitVar[Keystore]
    values: list = field(default_factory=list)

    def __post_init__(self, key, keystore):
        self.key = key
        self.keystore = keystore

    def add(self, added_values):
        values = set(self.values)
        values.update(set(added_values))
        document = self.keystore.inventory.document(self.key)
        document.set({"values": sorted(list(values))}, merge=True)


@dataclass
class Key:
    key_id: InitVar[str]
    keystore: InitVar[Keystore]
    email: str
    name: str
    campaigns: list = field(default_factory=list)
    is_restricted: bool = True
    services: list = field(default_factory=["*.*"])
    status: str = "active"

    def __post_init__(self, key_id, keystore):
        # These are defined as InitVar so that they are not part of the pickled data, and aren't
        # included in the to_dict() representation.
        self.key_id = key_id
        self.keystore = keystore

    def activate(self):
        self.update(status="active")

    def deactivate(self):
        self.update(status="inactive")

    def has_access(self, service, operation):
        """Check whether the service and operation are granted access by this Key."""
        if self.status != "active":
            return False

        for grant in self.services:
            grant = dict(zip(("service", "operation"), grant.split(".")))
            if grant["service"] == "*":
                return True
            elif grant["service"] == service and grant["operation"] == "*":
                return True
            elif grant["service"] == service and grant["operation"] == operation:
                return True

        return False

    def to_dict(self):
        return asdict(self)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__annotations__.keys() and key not in ("key_id", "keystore"):
                setattr(self, key, value)

        self.keystore.update_key(self, self.to_dict())


def fake_key(
    key_id,
    campaigns=None,
    email=None,
    is_restricted=True,
    name=None,
    services=None,
    status="active",
):
    return Key(
        keystore=mock.Mock(spec_set=Keystore),
        key_id=key_id,
        campaigns=campaigns or [],
        email=email or "john.doe@rip.com",
        is_restricted=is_restricted,
        name=name or "John Doe",
        services=services if services is not None else ["*.*"],
        status=status,
    )
