from sqlalchemy import ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from bank.orm.base_orm import Base


# class TransactionOrm(Base):

#     __tablename__ = "transactions"

#     id: Mapped[int] = mapped_column(
#         Integer(), primary_key=True, autoincrement=True, unique=True
#     )
#     id_account_debtor: Mapped[int] = mapped_column(
#         ForeignKey("accounts.id"), nullable=False
#     )
#     id_account_recipient: Mapped[int] = mapped_column(
#         ForeignKey("accounts.id"), nullable=False
#     )
#     account_debtor: Mapped["AccountOrm"] = relationship(
#         "AccountOrm", foreign_keys=[id_account_debtor]
#     )
#     account_recipent: Mapped["AccountOrm"] = relationship(
#         "AccountOrm", foreign_keys=[id_account_recipient]
#     )
#     amount: Mapped[float] = mapped_column(Float())
#     date: Mapped[DateTime] = mapped_column(
#         DateTime(), nullable=False, default=datetime.datetime.now()
#     )
