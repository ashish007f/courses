from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.customer_service import CustomerService
from ..core.database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])

def get_customer_service(db: AsyncSession = Depends(get_db)):
    return CustomerService(db)

@router.post("/simulate")
async def simulate_customer(service: CustomerService = Depends(get_customer_service)):
    customer = await service.create_random_customer()
    return {"status": "success", "customer": {
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "status": customer.status
    }}
