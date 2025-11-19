from datetime import datetime

from models import Account, Transaction, TransferRequest, TransferResponse
from database import accounts_by_id, transactions_by_account


class TransferService:
    @staticmethod
    def get_exchange_rate(source_currency: str, target_currency: str) -> float:
        """
        Tassi di cambio simulati.
        In un contesto reale verrebbero presi da un servizio esterno.
        """
        if source_currency == target_currency:
            return 1.0

        # Esempio semplificato: EUR <-> USD
        if source_currency == "EUR" and target_currency == "USD":
            return 1.1
        if source_currency == "USD" and target_currency == "EUR":
            return 0.9

        # Default (nessuna coppia specificata): tasso 1:1
        return 1.0

    @staticmethod
    def execute_transfer(payload: TransferRequest) -> TransferResponse:
        # Recuperiamo i conti
        source = accounts_by_id.get(payload.source_account_id)
        target = accounts_by_id.get(payload.target_account_id)

        if source is None or target is None:
            raise ValueError("Conto sorgente o destinazione inesistente")

        if payload.amount <= 0:
            raise ValueError("L'importo deve essere positivo")

        if source.balance < payload.amount:
            raise ValueError("Fondi insufficienti sul conto sorgente")

        # Calcolo del tasso di cambio
        rate = TransferService.get_exchange_rate(source.currency, target.currency)
        credited_amount = payload.amount * rate

        # Aggiornamento dei saldi
        source.balance -= payload.amount
        target.balance += credited_amount

        # Aggiornamento delle transazioni
        now = datetime.now()
        debit_tx = Transaction(
            id=len(transactions_by_account.get(source.id, [])) + 1,
            account_id=source.id,
            type="DEBIT",
            amount=payload.amount,
            currency=source.currency,
            description=f"Trasferimento verso conto {target.id}",
            created_at=now,
        )
        credit_tx = Transaction(
            id=len(transactions_by_account.get(target.id, [])) + 1,
            account_id=target.id,
            type="CREDIT",
            amount=credited_amount,
            currency=target.currency,
            description=f"Trasferimento da conto {source.id}",
            created_at=now,
        )

        transactions_by_account.setdefault(source.id, []).append(debit_tx)
        transactions_by_account.setdefault(target.id, []).append(credit_tx)

        return TransferResponse(
            source_account_id=source.id,
            target_account_id=target.id,
            amount=payload.amount,
            exchange_rate=rate,
            credited_amount=credited_amount,
            new_source_balance=source.balance,
            new_target_balance=target.balance,
        )
