from pydantic import BaseModel
from typing import List
from datetime import datetime

class User(BaseModel):
 id: int
 name: str
 email: str

class Account(BaseModel):
 id: int
 user_id: int
 currency: str
 balance: float

class Transaction(BaseModel):
 id: int
 account_id: int
 type: str # "DEBIT" o "CREDIT"
 amount: float
 currency: str
 description: str
 created_at: datetime

class AccountResponse(BaseModel):
 id: int
 currency: str
 balance: float

class TransactionResponse(BaseModel):
 id: int
 type: str
 amount: float
 currency: str
 description: str
 created_at: datetime

class TransferRequest(BaseModel):
 source_account_id: int
 target_account_id: int
 amount: float

class TransferResponse(BaseModel):
 source_account_id: int
 target_account_id: int
 amount: float
 exchange_rate: float
 credited_amount: float
 new_source_balance: float
 new_target_balance: float
