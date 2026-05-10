from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.db_models import DBAccount, DBBalance, DBTransaction, DBOutbox, TransactionType
from ..core.exceptions import InsufficientFundsError
from datetime import datetime, timezone
import uuid
import random

class BankingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, customer_id: uuid.UUID):
        async with self.db.begin():
            now = datetime.now(timezone.utc)
            account = DBAccount(
                id=uuid.uuid4(),
                customer_id=customer_id,
                account_number=f"ACC-{random.randint(1000000000, 9999999999)}",
                status="ACTIVE",
                currency="USD",
                created_at=now
            )
            self.db.add(account)
            
            # Initialize balance
            balance = DBBalance(account_id=account.id, amount=0.0, updated_at=now)
            self.db.add(balance)

            # Outbox event
            outbox_event = DBOutbox(
                topic="accounts",
                occurred_at=now,
                payload={
                    "id": str(account.id),
                    "customer_id": str(customer_id),
                    "account_number": account.account_number,
                    "status": account.status,
                    "currency": account.currency,
                    "created_time": str(now)
                }
            )
            self.db.add(outbox_event)
            
            return account

    async def process_transaction(self, account_id: uuid.UUID, amount: float, txn_type: TransactionType):
        async with self.db.begin():
            # 1. Fetch current balance with row-level locking (FOR UPDATE)
            stmt = select(DBBalance).filter_by(account_id=account_id).with_for_update()
            result = await self.db.execute(stmt)
            balance_record = result.scalar_one_or_none()
            
            if balance_record is None:
                # Mock create if not exists for the lab
                balance_record = DBBalance(account_id=account_id, amount=0.0)
                self.db.add(balance_record)
                await self.db.flush()

            # Ensure amount is treated as a float for calculations
            current_balance = float(balance_record.amount or 0.0) # type: ignore

            # 2. Validation
            if txn_type == TransactionType.WITHDRAWAL and current_balance < amount:
                raise InsufficientFundsError(str(account_id), current_balance, amount)

            delta = amount if txn_type == TransactionType.DEPOSIT else -amount
            new_balance = current_balance + delta

            now = datetime.now(timezone.utc)

            # 3. Update Balance
            balance_record.amount = new_balance # type: ignore
            balance_record.updated_at = now # type: ignore
            
            # Explicitly mark for update
            self.db.add(balance_record)

            # 4. Create Transaction Record
            txn = DBTransaction(
                id=uuid.uuid4(),
                account_id=account_id,
                amount=amount,
                type=txn_type.value,
                reference=f"REF-{uuid.uuid4().hex[:8].upper()}",
                occurred_at=now
            )
            self.db.add(txn)

            # 5. Insert into OUTBOX
            self.db.add(DBOutbox(
                topic="transactions",
                occurred_at=now,
                payload={
                    "id": str(txn.id),
                    "account_id": str(account_id),
                    "type": str(txn.type),
                    "amount": float(txn.amount or 0.0), # type: ignore
                    "reference": str(txn.reference),
                    "created_time": str(now)
                }
            ))

            self.db.add(DBOutbox(
                topic="balances",
                occurred_at=now,
                payload={
                    "account_id": str(account_id),
                    "new_balance": float(new_balance),
                    "delta": float(delta),
                    "transaction_id": str(txn.id),
                    "created_time": str(now)
                }
            ))

            # Ensure all changes are flushed to the transaction before commit (handled by context manager)
            await self.db.flush()

            return txn, new_balance
