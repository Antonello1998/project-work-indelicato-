from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models import (
    AccountResponse,
    TransactionResponse,
    TransferRequest,
    TransferResponse,
)
from database import users, accounts_by_user, accounts_by_id, transactions_by_account
from services import TransferService


app = FastAPI(
    title="Revolut-Style API",
    description="Prototipo di API per dashboard multivaluta ispirata a Revolut",
    version="1.0.0",
)

# CORS per permettere richieste da index.html
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/users/{user_id}/accounts", response_model=List[AccountResponse])
def get_accounts(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    accounts = accounts_by_user.get(user_id, [])
    return [
        AccountResponse(id=a.id, currency=a.currency, balance=a.balance)
        for a in accounts
    ]


@app.get(
    "/api/accounts/{account_id}/transactions",
    response_model=List[TransactionResponse],
)
def get_transactions(account_id: int):
    # prima controllo che il conto esiste
    if account_id not in accounts_by_id:
        raise HTTPException(status_code=404, detail="Conto non trovato")

    txs = transactions_by_account.get(account_id, [])
    return [
        TransactionResponse(
            id=t.id,
            type=t.type,
            amount=t.amount,
            currency=t.currency,
            description=t.description,
            created_at=t.created_at,
        )
        for t in txs
    ]


@app.post("/api/transfers", response_model=TransferResponse, status_code=201)
def transfer(request: TransferRequest):
    try:
        result = TransferService.execute_transfer(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
