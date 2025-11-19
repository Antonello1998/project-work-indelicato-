from datetime import datetime
from typing import Dict, List

from models import User, Account, Transaction

# In un sistema reale queste informazioni risiederebbero in un database.
# Qui vengono simulate in memoria per semplicità.

users: Dict[int, User] = {
    1: User(id=1, name="Mario Rossi", email="mario.rossi@example.com")
}

accounts_by_user: Dict[int, List[Account]] = {
    1: [
        Account(id=101, user_id=1, currency="EUR", balance=1000.0),
        Account(id=102, user_id=1, currency="USD", balance=500.0),
    ]
}

# Indicizziamo i conti anche per id, per accesso diretto
accounts_by_id: Dict[int, Account] = {
    acc.id: acc
    for user_accounts in accounts_by_user.values()
    for acc in user_accounts
}

transactions_by_account: Dict[int, List[Transaction]] = {
    101: [
        Transaction(
            id=1,
            account_id=101,
            type="CREDIT",
            amount=1000.0,
            currency="EUR",
            description="Deposito iniziale",
            created_at=datetime.now(),
        )
    ],
    102: [
        Transaction(
            id=2,
            account_id=102,
            type="CREDIT",
            amount=500.0,
            currency="USD",
            description="Deposito iniziale",
            created_at=datetime.now(),
        )
    ],
}
