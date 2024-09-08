from bank.pojo.base_model import Base, Device
from abc import ABC
from datetime import datetime
from pydantic import model_validator, field_validator


class AccountType(ABC):
    pass


class Account(Base):
    ## TODO LATER   account_type: AccountType
    bank_overdraft: None | float = None
    amount: float
    client_id: int
    opening_date: None | datetime = None

    @model_validator(mode="after")
    @classmethod
    def amount_not_exceed_overdraft(cls, values):
        amount = values.amount
        bank_overdraft = values.bank_overdraft
        if (bank_overdraft is not None and amount < bank_overdraft) or (
            bank_overdraft is None and amount < 0
        ):
            raise ValueError("Init amount can't be above overdraft level")
        return values


class AccountIn(Account):
    pass


class AccountOut(Account):
    id: int
