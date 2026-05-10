from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from enum import Enum
from ..core.database import Base

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"

class DBOutbox(Base):
    __tablename__ = "outbox"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DBCustomer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DBAccount(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    account_number = Column(String, unique=True)
    status = Column(String, default="ACTIVE")
    currency = Column(String, default="USD")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DBBalance(Base):
    __tablename__ = "balances"
    account_id = Column(UUID(as_uuid=True), primary_key=True)
    amount = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class DBTransaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("balances.account_id"))
    amount = Column(Float)
    type = Column(String)
    reference = Column(String)
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
