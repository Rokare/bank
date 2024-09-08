from pytest import raises
from bank.pojo.client_model import Client, ClientIn
from bank.pojo.account_model import Account, AccountIn, AccountOut, Device
from bank.dao.account_dao import AccountDao
from bank.dao.client_dao import ClientDao
from bank.pojo.transaction_model import TransactionIn
from bank.dao.transaction_dao import TransactionDao
import pytest


@pytest.fixture(scope="function", autouse=True)
def create_one_client_and_account(session):
    ClientDao(session).create(ClientIn(first_name="Jeanne", last_name="test", age=15))
    AccountDao(session).create(
        AccountIn(amount=750.51, client_id=1, bank_overdraft=-50)
    )
    AccountDao(session).create(AccountIn(amount=0, client_id=1, bank_overdraft=0))


@pytest.fixture
def create_two_client_and_account(session):
    ClientDao(session).create(ClientIn(first_name="Jeanne", last_name="test", age=15))
    ClientDao(session).create(ClientIn(first_name="test", last_name="test", age=100))
    AccountDao(session).create(
        AccountIn(amount=750.51, client_id=1, bank_overdraft=-50)
    )
    AccountDao(session).create(AccountIn(amount=0, client_id=2, bank_overdraft=0))


def test_create_transaction_between_same_client(session):
    transaction_orm = TransactionDao(session).create(
        TransactionIn(id_account_debtor=1, id_account_recipient=2, amount=50)
    )
    assert transaction_orm.id == 1
    assert transaction_orm.amount == 50
    account_orm = AccountDao(session).get_by_id(2)
    assert account_orm.amount == 50


@pytest.mark.usefixtures("create_two_client_and_account")
def test_create_transaction_between_two_clients(session):
    transaction_orm = TransactionDao(session).create(
        TransactionIn(id_account_debtor=1, id_account_recipient=2, amount=50)
    )
    assert transaction_orm.id == 1
    assert transaction_orm.amount == 50
    account_orm = AccountDao(session).get_by_id(2)
    assert account_orm.amount == 50
    assert account_orm.client.first_name == "Jeanne"


def test_transaction_above_overdraft(session):
    pass


def test_get_all_transactions_from_account(session):
    test_create_transaction_between_same_client(session)
    transactions_orm = TransactionDao(session).get_transactions_by_account(2)
    assert transactions_orm[0].id == 1
    assert len(transactions_orm) == 1


def test_get_a_transaction(session):
    test_create_transaction_between_same_client(session)
    transaction_dao = TransactionDao(session).get_by_id(1)
    assert transaction_dao.id == 1
    assert transaction_dao.amount == 50


## NO USE
# def test_delete_a_transaction(session):
#     pass


# def test_delete_all_transactions_from_account(session):
#     pass
