from sqlalchemy import select
from bank.pojo.account_model import AccountIn, AccountOut, Account
from bank.orm.object_orm import AccountOrm
from bank.orm.object_orm import ClientOrm
from bank.orm.object_orm import TransactionOrm
from bank.pojo.client_model import Client
from bank.dao.exception import ValueNotFound
from typing import List
from bank.dao.base_dao import FullBaseDao
from sqlalchemy import or_


class AccountDao(FullBaseDao):
    def __init__(self, session) -> None:
        self.session = session

    def create(self, account: Account) -> AccountOrm:
        ac = AccountOrm(**account.model_dump(exclude_unset=True))
        self.session.add(ac)
        self.session.commit()
        self.session.refresh(ac)
        return ac

    def get_all(self) -> List[AccountOrm]:
        accounts = self.session.query(AccountOrm).all()
        return accounts

    def get_by_id(self, id: int) -> AccountOrm:
        statement = select(AccountOrm).where(AccountOrm.id == id)
        account = self.session.scalar(statement)
        return account

    def get_by_client(self, client: Client) -> List[AccountOrm]:
        client_orm = self.session.get(ClientOrm, client.id)
        return client_orm.accounts

    def get_by_id_client(self, id_client: int) -> List[AccountOrm]:
        client_orm = self.session.get(ClientOrm, id_client)
        return client_orm.accounts

    def modify(self, id: int, account: AccountIn):
        account_orm = self.session.get(AccountOrm, id)
        for key, value in account.__dict__.items():
            setattr(account_orm, key, value)
        self.session.commit()
        self.session.refresh(account_orm)
        return account_orm

    def delete_account_transactions(self, id: int):
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
        for t in transactions:
            self.session.delete(t)
        self.session.commit()

    def delete_by_id(self, id: int) -> AccountOrm:
        account = self.session.get(AccountOrm, id)
        self.delete_account_transactions(id)
        self.session.delete(account)
        self.session.commit()
        if self.session.get(AccountOrm, id) is None:
            return True
        else:
            return False

    def delete_all_account_by_id_client(self, id: int):
        accounts = self.get_by_id_client(id)
        for account in accounts:
            self.delete_account_transactions(account.id)
            self.session.delete(account)
        self.session.commit()
        if len(self.get_by_id_client(id)) == 0:
            return True
        else:
            return False

    def delete_all(self):
        pass
