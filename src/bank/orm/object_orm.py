from sqlalchemy import ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from typing import List
from bank.orm.base_orm import Base
from sqlalchemy.orm import validates

# from bank.orm.register_orm import mapper_registry


class AccountOrm(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, autoincrement=True, unique=True
    )
    bank_overdraft: Mapped[float] = mapped_column(Float(), default=0)
    amount: Mapped[float] = mapped_column(Float())
    opening_date: Mapped[DateTime] = mapped_column(
        DateTime(), nullable=False, default=datetime.datetime.now()
    )
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["ClientOrm"] = relationship(
        "ClientOrm", back_populates="accounts", foreign_keys=[client_id]
    )


class ClientOrm(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )
    opening_date: Mapped[DateTime] = mapped_column(
        DateTime(), nullable=False, default=datetime.datetime.now()
    )
    ## Need to solve circular import or reput all object in same file
    accounts: Mapped[List["AccountOrm"]] = relationship(
        "AccountOrm", back_populates="client", cascade="all, delete"
    )

    @validates("age")
    def validate_age(self, key, age):
        if age <= 0:
            raise ValueError("L'âge ne peut pas être négatif ou égal à 0.")
        if age > 120:
            raise ValueError("L'âge doit être réaliste (moins de 120 ans).")
        return age


class TransactionOrm(Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, autoincrement=True, unique=True
    )
    id_account_debtor: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )
    id_account_recipient: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False
    )
    account_debtor: Mapped["AccountOrm"] = relationship(
        "AccountOrm",
        foreign_keys=[id_account_debtor],
    )
    account_recipent: Mapped["AccountOrm"] = relationship(
        "AccountOrm",
        foreign_keys=[id_account_recipient],
    )
    amount: Mapped[float] = mapped_column(Float())
    date: Mapped[DateTime] = mapped_column(
        DateTime(), nullable=False, default=datetime.datetime.now()
    )
