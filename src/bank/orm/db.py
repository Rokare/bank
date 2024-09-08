from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bank.orm.base_orm import Base


__DATABASE_URL = "postgresql://user:test123@localhost:5432/bank"
engine = create_engine(__DATABASE_URL)


def init_session():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


def get_db_session():
    with init_session() as session:
        yield session


def drop_db():
    Base.metadata.drop_all(engine)
