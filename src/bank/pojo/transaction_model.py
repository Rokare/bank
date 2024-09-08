from bank.pojo.base_model import Base
from abc import ABC


class TransactionType(ABC):
    pass


class Transaction(Base):
    ## TODO LATER   transaction_type: TransactionType
    id_account_debtor: int
    id_account_recipient: int
    amount: float


class TransactionIn(Transaction):
    pass


class TransactionOut(Transaction):
    id: int
