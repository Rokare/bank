import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bank.orm.base_orm import Base
from bank.orm.object_orm import AccountOrm, ClientOrm


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")  # Utilisation de SQLite en mémoire


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    yield session
    session.rollback()  # Annule toutes les transactions après chaque test
    session.close()
    Base.metadata.drop_all(engine)
