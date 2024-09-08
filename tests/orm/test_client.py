from pytest import raises
from bank.dao.client_dao import ClientDao
from bank.pojo.client_model import ClientIn, ClientOut
from bank.dao.exception import ValueNotFound


def create_client(session):
    ClientDao(session).create(ClientIn(first_name="Jeanne", last_name="test", age=15))


def test_create_client(session):
    c = ClientIn(first_name="Jean", last_name="Jacques", age=15)
    client = ClientDao(session).create(c)
    # Récupération de l'utilisateur
    assert client is not None
    assert client.first_name == "Jean"
    assert client.last_name == "Jacques"
    assert client.id is not None
    assert client.id == 1


def test_wrong_age_client(session):
    with raises(ValueError):
        ClientDao(session).create(
            ClientIn(first_name="Jean", last_name="Jacques", age=-3)
        )


def test_get_client_with_bad_name(session):
    create_client(session)
    with raises(ValueNotFound):
        ClientDao(session).get_by_fullname(first_name="test", last_name="test")


def test_modify_client(session):
    create_client(session)
    clientOrm = ClientDao(session).get_by_id(1)
    client = ClientOut.model_validate(clientOrm.__dict__)
    client.age = 100
    client.first_name = "test"
    modify_client = ClientDao(session).modify(clientOrm.id, client)
    assert modify_client.age == 100
    assert modify_client.last_name != "Jeanne"


def test_delete_client_by_id(session):
    create_client(session)
    is_deleted = ClientDao(session).delete_by_id(1)
    assert is_deleted


def test_delete_client(session):
    create_client(session)
    c = ClientOut(id=1, first_name="Jeanne", last_name="test", age=15)
    is_deleted = ClientDao(session).delete(c)
    assert is_deleted


# TODO
def test_get_all_clients(session):
    pass


# TODO
def test_delete_client_with_account(session):
    pass
