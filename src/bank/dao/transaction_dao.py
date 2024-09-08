from bank.pojo.transaction_model import TransactionIn
from bank.orm.object_orm import TransactionOrm
from bank.dao.account_dao import AccountDao
from bank.dao.base_dao import BaseDao
from sqlalchemy import or_
from typing import List


class TransactionDao(BaseDao):
    def __init__(self, session) -> None:
        self.session = session

    def create(self, transaction: TransactionIn) -> TransactionOrm:
        transaction_orm = TransactionOrm(**transaction.model_dump())
        if not self.check_account_exist(transaction):
            raise ValueError("One of the account doesn't exist")
        if not self.transaction_not_exceed_account_overdraft(
            transaction_orm.id_account_debtor, transaction_orm.amount
        ):
            self.session.add(transaction_orm)
            self.session.commit()
            if self.get_by_id(transaction_orm.id) is not None:
                self.update_account_with_transaction(transaction_orm)
                self.session.refresh(transaction_orm)
                return transaction_orm
        else:
            raise ValueError("Transaction amound is exceed overdraft of deptor account")

    def check_account_exist(self, transaction: TransactionIn):
        account_debtor = AccountDao(self.session).get_by_id(
            transaction.id_account_debtor
        )
        account_recipient = AccountDao(self.session).get_by_id(
            transaction.id_account_recipient
        )
        return account_debtor is not None or account_recipient is not None

    def transaction_not_exceed_account_overdraft(
        self, account_id: int, amount: float
    ) -> bool:
        account_orm = AccountDao(self.session).get_by_id(account_id)
        if (account_orm.amount - amount) < account_orm.bank_overdraft:
            return True
        else:
            return False

    def get_by_id(self, id: int) -> TransactionOrm:
        return self.session.get(TransactionOrm, id)

    def get_transactions_by_account(self, id: int) -> List[TransactionOrm]:
        transactions = (
            self.session.query(TransactionOrm)
            .filter(
                or_(
                    TransactionOrm.id_account_debtor == id,
                    TransactionOrm.id_account_recipient == id,
                )
            )
            .all()
        )
        if transactions is None or len(transactions) == 0:
            raise ValueError("qsdqsdd")
        return transactions

    def update_account_with_transaction(self, transactionOrm: TransactionOrm):
        transactionOrm.account_debtor.amount = (
            transactionOrm.account_debtor.amount - transactionOrm.amount
        )
        transactionOrm.account_recipent.amount = (
            transactionOrm.account_recipent.amount + transactionOrm.amount
        )
        self.session.merge(transactionOrm.account_debtor)
        self.session.merge(transactionOrm.account_recipent)
        self.session.commit()

    def get_all(self) -> List[TransactionOrm]:
        transaction = self.session.query(TransactionOrm).all()
        return transaction

    ## NO use transaction need stay, will be delete only if one of the account is deleted
    # def delete(self, id: int):
    #     pass

    # def delete_all_from_account(self):
    #     pass
