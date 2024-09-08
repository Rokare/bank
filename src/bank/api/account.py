from fastapi import APIRouter, status, HTTPException
from bank.pojo.account_model import AccountIn, AccountOut
from sqlalchemy.orm import Session
from fastapi import Depends
from bank.orm.db import get_db_session
from bank.dao.account_dao import AccountDao
from bank.dao.client_dao import ClientDao
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


@account_router.get("/get_accounts/{id_client}", status_code=status.HTTP_200_OK)
def get_accounts_from_id_client(
    id_client: int, session: Session = Depends(get_db_session)
) -> List[AccountOut]:
    accounts_dao = AccountDao(session).get_by_id_client(id_client)
    list_accounts = []
    for a in accounts_dao:
        list_accounts.append(AccountOut.model_validate(a.__dict__))
    return list_accounts


@account_router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountIn, session: Session = Depends(get_db_session)
) -> AccountOut:
    try:
        client_dao = ClientDao(session).get_by_id(account.client_id)
        account_dao = AccountDao(session).create(account)
        account_out = AccountOut.model_validate(account_dao.__dict__)
        return account_out
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


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
