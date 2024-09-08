from fastapi import FastAPI
from bank.api.client import client_router
from bank.api.account import account_router
from bank.api.transaction import transaction_router

app = FastAPI()
app.include_router(client_router)
app.include_router(account_router)
app.include_router(transaction_router)
