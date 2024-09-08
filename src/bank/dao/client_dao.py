from bank.orm.object_orm import ClientOrm
from bank.orm.object_orm import AccountOrm
from sqlalchemy import select
from bank.pojo.client_model import Client, ClientOut, ClientIn
from bank.dao.exception import ValueNotFound
from typing import List
import logging
from bank.dao.base_dao import FullBaseDao

LOG = logging.getLogger("__nom__")


class ClientDao(FullBaseDao):
    def __init__(self, session) -> None:
        self.session = session

    def create(self, client: Client) -> ClientOrm:
        client_orm = ClientOrm(**client.model_dump())
        if client_orm.id is not None:
            raise AttributeError("L'id ne doit pas être initialiser")
        self.session.add(client_orm)
        self.session.commit()
        self.session.refresh(client_orm)
        return client_orm

    def get_all(self) -> List[ClientOrm]:
        clients = self.session.query(ClientOrm).all()
        return clients

    def get_by_id(self, id: int) -> ClientOrm:
        client = self.session.get(ClientOrm, id)
        if client is not None:
            return client
        else:
            raise ValueNotFound(f"unable to find a client with id : {id}")

    def get_by_fullname(self, first_name: str, last_name: str) -> ClientOrm:
        client = self.session.execute(
            select(ClientOrm).filter_by(first_name=first_name, last_name=last_name)
        ).first()
        if client is not None:
            return client
        else:
            raise ValueNotFound(
                f"unable to find a client with : {first_name} {last_name}"
            )

    def modify(self, id: int, client: ClientIn) -> ClientOrm:
        client_orm = self.session.get(ClientOrm, id)
        if client_orm is not None:
            for key, value in client.__dict__.items():
                setattr(client_orm, key, value)
            self.session.commit()
            self.session.refresh(client_orm)
            return client_orm
        else:
            raise ValueNotFound(f"unable to find a client with id : {id}")

    def delete_by_id(self, id: int) -> ClientOrm:
        client = self.session.get(ClientOrm, id)
        if client is not None:
            self.session.delete(client)
            self.session.commit()
            if self.session.get(ClientOrm, id) is None:
                return True
            else:
                return False
        else:
            raise ValueNotFound(f"unable to find a client with id : {id}")

    def delete_all(self):
        pass

    def delete(self, client: ClientOut) -> bool:
        clientOrm = self.session.get(ClientOrm, client.id)
        if clientOrm is not None:
            self.session.delete(clientOrm)
            self.session.commit()
            if self.session.get(ClientOrm, clientOrm.id) is None:
                return True
            else:
                return False
