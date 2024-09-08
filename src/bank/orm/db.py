from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bank.orm.base_orm import Base
from bank.settings import settings


engine = create_engine(settings.database_uri.unicode_string())


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
