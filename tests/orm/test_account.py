from pytest import raises
from bank.pojo.client_model import Client, ClientIn
from bank.pojo.account_model import Account, AccountIn, AccountOut, Device
from bank.dao.account_dao import AccountDao
from bank.dao.client_dao import ClientDao
import pytest


@pytest.fixture(scope="function", autouse=True)
def create_one_client(session):
    ClientDao(session).create(ClientIn(first_name="Jeanne", last_name="test", age=15))


# @pytest.mark.usefixtures('fixture_name_here')
# test_name(session):


def test_create_account(session):
    account = AccountDao(session).create(
        AccountIn(amount=750.51, client_id=1, bank_overdraft=-50)
    )
    assert account.amount == 750.51


def test_create_account_overdraft(session):
    with raises(ValueError):
        AccountDao(session).create(
            AccountIn(amount=-150, client_id=1, bank_overdraft=-100)
        )


def test_get_accounts(session):
    accountOrm = AccountDao(session).create(AccountIn(amount=750.51, client_id=1))
    accountOrm2 = AccountDao(session).create(AccountIn(amount=55555, client_id=1))
    accounts = AccountDao(session).get_by_id_client(1)
    assert len(accounts) == 2
    assert accounts[0].amount == 750.51


def test_modify_account(session):
    accountOrm = AccountDao(session).create(AccountIn(amount=750.51, client_id=1))
    account = AccountIn.model_validate(accountOrm.__dict__)
    account.amount = 150
    modify_account = AccountDao(session).modify(accountOrm.id, account)
    assert modify_account.amount == 150


def test_delete_acccount(session):
    accountOrm = AccountDao(session).create(AccountIn(amount=750.51, client_id=1))
    is_deleted = AccountDao(session).delete_by_id(accountOrm.id)
    assert is_deleted


def test_delete_all_account_client(session):
    accountOrm = AccountDao(session).create(AccountIn(amount=750.51, client_id=1))
    accountOrm2 = AccountDao(session).create(AccountIn(amount=55555, client_id=1))
    is_deleted = AccountDao(session).delete_all_account_by_id_client(1)
    assert is_deleted


def test_get_all_accounts(session):
    test_create_account(session)
    list_accounts = AccountDao(session).get_all()
    assert type(list_accounts) is list
    assert len(list_accounts) == 1


def test_delete_accounts_with_transactions(session):
    pass
