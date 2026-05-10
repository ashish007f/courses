from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.banking_service import BankingService
from ..models.db_models import TransactionType
from ..core.exceptions import InsufficientFundsError
from ..core.database import get_db
import uuid

router = APIRouter(tags=["banking"])

def get_banking_service(db: AsyncSession = Depends(get_db)):
    return BankingService(db)

@router.post("/accounts/{customer_id}")
async def create_account(customer_id: uuid.UUID, service: BankingService = Depends(get_banking_service)):
    account = await service.create_account(customer_id)
    return {"status": "success", "account": {
        "id": account.id,
        "customer_id": account.customer_id,
        "account_number": account.account_number,
        "status": account.status,
        "currency": account.currency
    }}

@router.post("/transactions/deposit/{account_id}")
async def deposit(account_id: uuid.UUID, amount: float, service: BankingService = Depends(get_banking_service)):
    transaction, new_balance = await service.process_transaction(
        account_id, amount, TransactionType.DEPOSIT
    )
    return {
        "status": "success", 
        "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "type": transaction.type,
            "reference": transaction.reference
        }, 
        "new_balance": new_balance
    }

@router.post("/transactions/withdraw/{account_id}")
async def withdraw(account_id: uuid.UUID, amount: float, service: BankingService = Depends(get_banking_service)):
    try:
        transaction, new_balance = await service.process_transaction(
            account_id, amount, TransactionType.WITHDRAWAL
        )
        return {
            "status": "success", 
            "transaction": {
                "id": transaction.id,
                "amount": transaction.amount,
                "type": transaction.type,
                "reference": transaction.reference
            }, 
            "new_balance": new_balance
        }
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
