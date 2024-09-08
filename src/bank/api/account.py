from fastapi import APIRouter, FastAPI, status
from bank.pojo.account_model import AccountIn, AccountOut, Account
from sqlalchemy.orm import Session
from fastapi import Depends
from bank.orm.db import get_db_session
from bank.dao.account_dao import AccountDao
from typing import List

account_router = APIRouter(tags=["Account"], prefix="/account")


@account_router.get("/", status_code=status.HTTP_200_OK)
def get_all_account(session: Session = Depends(get_db_session)) -> List[AccountOut]:
    accounts_dao = AccountDao(session).get_all()
    list_account_out = []
    for c in accounts_dao:
        list_account_out.append(AccountOut.model_validate(c.__dict__))
    return list_account_out


@account_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_account(id: int, session: Session = Depends(get_db_session)) -> AccountOut:
    account_dao = AccountDao(session).get_by_id(id)
    account_out = AccountOut.model_validate(account_dao.__dict__)
    return account_out


@account_router.post("/add", status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountIn, session: Session = Depends(get_db_session)
) -> AccountOut:
    account_dao = AccountDao(session).create(account)
    account_out = AccountOut.model_validate(account_dao.__dict__)
    return account_out


@account_router.put("/{id}", status_code=status.HTTP_200_OK)
def modify_client(
    id: int, account: AccountIn, session: Session = Depends(get_db_session)
) -> AccountOut:
    account_dao = AccountDao(session).modify(id, account)
    account_out = AccountOut.model_validate(account_dao.__dict__)
    return account_out


@account_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_account(id: int, session: Session = Depends(get_db_session)):
    is_deleted = AccountDao(session).delete_by_id(id)
    return {"Is_Deleted": is_deleted}
