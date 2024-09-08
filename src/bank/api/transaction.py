from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from bank.orm.db import get_db_session
from bank.dao.transaction_dao import TransactionDao
from bank.pojo.transaction_model import TransactionOut, TransactionIn
from typing import List
import logging

transaction_router = APIRouter(tags=["transaction"], prefix="/transaction")

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


@transaction_router.get("/", status_code=status.HTTP_200_OK)
def get_all_transactions(
    session: Session = Depends(get_db_session),
) -> List[TransactionOut]:
    transactions_dao = TransactionDao(session).get_all()
    list_transaction_out = []
    for c in transactions_dao:
        list_transaction_out.append(TransactionOut.model_validate(c.__dict__))
    return list_transaction_out


@transaction_router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionIn, session: Session = Depends(get_db_session)
) -> TransactionOut:
    transaction_dao = TransactionDao(session).create(transaction)
    transaction_out = TransactionOut.model_validate(transaction_dao.__dict__)
    return transaction_out


@transaction_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_transaction_by_id(
    id: int, session: Session = Depends(get_db_session)
) -> TransactionOut:
    logger.debug("this is a debug message")
    transaction_dao = TransactionDao(session).get_by_id(id)
    if transaction_dao is not None:
        transaction_out = TransactionOut.model_validate(transaction_dao.__dict__)
        return transaction_out
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction with the given id does not exist",
        )


@transaction_router.get("/from_account/{id_account}", status_code=status.HTTP_200_OK)
def get_transactions_by_account(
    id_account: int, session: Session = Depends(get_db_session)
) -> List[TransactionOut]:
    transactions_dao = TransactionDao(session).get_transactions_by_account(id_account)
    logger.debug(len(transactions_dao))
    list_transactions = []
    for t in transactions_dao:
        list_transactions.append(TransactionOut.model_validate(t.__dict__))
    return list_transactions
