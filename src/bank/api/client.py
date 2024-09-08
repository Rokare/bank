from fastapi import APIRouter, status, HTTPException
from bank.pojo.client_model import ClientIn, ClientOut, Client
from sqlalchemy.orm import Session
from fastapi import Depends
from bank.orm.db import get_db_session
from bank.dao.client_dao import ClientDao
from typing import List

client_router = APIRouter(tags=["Client"], prefix="/client")


@client_router.get("/", status_code=status.HTTP_200_OK)
def get_all_clients(session: Session = Depends(get_db_session)) -> List[ClientOut]:
    clients_dao = ClientDao(session).get_all()
    list_client_out = []
    for c in clients_dao:
        list_client_out.append(ClientOut.model_validate(c.__dict__))
    return list_client_out


@client_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_client(id: int, session: Session = Depends(get_db_session)) -> ClientOut:
    try:
        client_dao = ClientDao(session).get_by_id(id)
        client_out = ClientOut.model_validate(client_dao.__dict__)
        return client_out
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


@client_router.post("/", status_code=status.HTTP_201_CREATED)
def add_client(
    client: ClientIn, session: Session = Depends(get_db_session)
) -> ClientOut:
    client_dao = ClientDao(session).create(client)
    client_out = ClientOut.model_validate(client_dao.__dict__)
    return client_out


@client_router.put("/{id}", status_code=status.HTTP_200_OK)
def modify_client(
    id: int, client: Client, session: Session = Depends(get_db_session)
) -> ClientOut:
    try:
        client_dao = ClientDao(session).modify(id, client)
        client_out = ClientOut.model_validate(client_dao.__dict__)
        return client_out
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


@client_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_client(id: int, session: Session = Depends(get_db_session)):
    try:
        is_deleted = ClientDao(session).delete_by_id(id)
        return {"Is_Deleted": is_deleted}
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )
