class BankingError(Exception):
    """Base class for banking exceptions"""
    pass

class InsufficientFundsError(BankingError):
    """Raised when an account has insufficient funds for a withdrawal"""
    def __init__(self, account_id: str, current_balance: float, amount: float):
        self.account_id = account_id
        self.current_balance = current_balance
        self.amount = amount
        super().__init__(f"Account {account_id} has insufficient funds: {current_balance} < {amount}")
