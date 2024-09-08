from bank.pojo.base_model import Base
from datetime import datetime
from typing import Optional


class Client(Base):
    first_name: str
    last_name: str
    age: int
    opening_date: None | datetime = None


class ClientIn(Client):
    pass


class ClientOut(Client):
    id: int


## TO REWORK LATER
class ClientPatch(Client):
    first_name: Optional[str]
    last_name: str
    age: int
    opening_date: None | datetime = None
