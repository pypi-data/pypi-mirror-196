from __future__ import annotations

from datetime import datetime
from typing import Any

from citext import CIText
from sqlalchemy import ARRAY, JSON, Column
from sqlalchemy import Column, DateTime, String

from sqlalchemy import (
    String,
    Text,
    TypeDecorator,
    cast,
    type_coerce,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql import func

from fides.lib.db.base_class import Base

from fides.core.config import FidesConfig, get_config

CONFIG: FidesConfig = get_config()

class PGEncryptedString(TypeDecorator):
    """
    This TypeDecorator handles encrypting and decrypting values at rest
    on the database that would normally be stored as json.

    The values are explicitly cast as json then text to take advantage of
    the pgcrypto extension.
    """

    impl = BYTEA
    python_type = String

    cache_ok = True

    def __init__(self):
        super().__init__()

        self.passphrase = CONFIG.user.encryption_key

    def bind_expression(self, bindparam):
        # Needs to be a string for the encryption, however it also needs to be treated as JSON first

        bindparam = type_coerce(bindparam, JSON)

        return func.pgp_sym_encrypt(cast(bindparam, Text), self.passphrase)

    def column_expression(self, column):
        return cast(func.pgp_sym_decrypt(column, self.passphrase), JSON)

    def process_bind_param(self, value, dialect):
        pass

    def process_literal_param(self, value, dialect):
        pass

    def process_result_value(self, value, dialect):
        pass

class Ctl_Organizations(Base):
    """The DB ORM model for M3LD Organization."""

    organization_fides_key = Column(CIText, unique=True, index=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    organization_parent_key = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    controller = Column(PGEncryptedString, nullable=True)
    data_protection_officer = Column(PGEncryptedString, nullable=True)
    representative = Column(PGEncryptedString, nullable=True)
    security_policy = Column(String, nullable=True)
    fidesctl_meta = Column(JSON)
    tags = Column(ARRAY(String))