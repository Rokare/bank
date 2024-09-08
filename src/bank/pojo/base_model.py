from pydantic import BaseModel, ConfigDict
from enum import Enum


class Base(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Device(Enum):
    EUR = "€"
    USD = "$"
    GPB = "£"
