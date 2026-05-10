from sqlalchemy.ext.asyncio import AsyncSession
from ..models.db_models import DBCustomer, DBOutbox
from faker import Faker
import uuid
from datetime import datetime, timezone

faker = Faker()

class CustomerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_random_customer(self):
        async with self.db.begin():
            now = datetime.now(timezone.utc)
            customer = DBCustomer(
                id=uuid.uuid4(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.unique.email(),
                status="ACTIVE",
                created_at=now
            )
            self.db.add(customer)

            # Insert into OUTBOX
            outbox_event = DBOutbox(
                topic="customers",
                occurred_at=now,
                payload={
                    "id": str(customer.id),
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "email": customer.email,
                    "status": customer.status,
                    "created_time": str(now)
                }
            )
            self.db.add(outbox_event)
            
            return customer
