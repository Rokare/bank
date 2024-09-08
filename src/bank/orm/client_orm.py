from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from typing import List
from sqlalchemy.orm import validates
from bank.orm.base_orm import Base


# class ClientOrm(Base):
#     __tablename__ = "clients"

#     id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
#     first_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     age: Mapped[int] = mapped_column(
#         Integer(),
#         nullable=False,
#     )
#     opening_date: Mapped[DateTime] = mapped_column(
#         DateTime(), nullable=False, default=datetime.datetime.now()
#     )
#     ## Need to solve circular import or reput all object in same file
#     accounts: Mapped[List["AccountOrm"]] = relationship(
#         "AccountOrm", back_populates="client"
#     )

#     @validates("age")
#     def validate_age(self, key, age):
#         if age < 0:
#             raise ValueError("L'âge ne peut pas être négatif.")
#         if age > 120:
#             raise ValueError("L'âge doit être réaliste (moins de 120 ans).")
#         return age
