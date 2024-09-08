from fastapi import FastAPI
from fastapi.testclient import TestClient
from bank.api.main import app
from faker import Faker
from bank.pojo.client_model import ClientOut

# from .fixtures import mock_requests_get
from unittest.mock import patch

client = TestClient(app)
faker = Faker()


# @pytest.fixture
# @patch("bank.api.client.get_client")
# @patch("bank.dao.ClientDao")
# def test_get_a_client(ClientDAOMock):
#     # ClientDAOMock.get_by_Id.return_value = ClientOrm(id=15, ...)

#     response = client.get("/client/15")
#     assert response.status_code == 200
#     assert response.json() == ClientOrm.model_dump()
#     assert ClientDAOMock.__init__.called
#     assert ClientDAOMock.get_by_Id.called


# app.dependency_overrides[get_client] = mock_get_a_client


# def test_get_client():

#     response = client.get("/client/")
#     print(response)
#     assert response.status_code == 200
#     print(response.json())
#     client_data = ClientOut(**response.json())
#     # print(client_data)
#     assert response.json() == {
#         {
#             mock_get_a_client
#             # "id": 1,
#             # "first_name": fake_first_name,
#             # "last_name": fake_last_name,
#             # "opening_date": fake_opening_date,
#         },
#     }


# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
