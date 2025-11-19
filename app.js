// app.js

async function loadAccounts() {
    const userIdInput = document.getElementById("userId");
    const userId = Number(userIdInput.value);

    if (!userId) {
        alert("Inserisci un ID utente valido");
        return;
    }

    const tableBody = document.querySelector("#accountsTable tbody");
    const accountSelect = document.getElementById("accountSelect");

    tableBody.innerHTML = "";
    accountSelect.innerHTML = '<option value="">-- nessun conto --</option>';

    try {
        const res = await fetch(`${API_BASE}/api/users/${userId}/accounts`);

        if (!res.ok) {
            alert("Errore nel caricamento dei conti (utente non trovato?)");
            return;
        }

        const data = await res.json();

        data.forEach(acc => {
            const balance = Number(acc.balance);

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${acc.id}</td>
                <td>${acc.currency}</td>
                <td>${balance.toFixed(2)}</td>
            `;
            tableBody.appendChild(tr);

            const opt = document.createElement("option");
            opt.value = acc.id;
            opt.textContent = `${acc.id} (${acc.currency})`;
            accountSelect.appendChild(opt);
        });
    } catch (err) {
        console.error(err);
        alert("Errore di rete nel caricamento dei conti");
    }
}

async function loadTransactions() {
    const accountSelect = document.getElementById("accountSelect");
    const accountId = accountSelect.value;

    if (!accountId) {
        alert("Seleziona un conto");
        return;
    }

    const tableBody = document.querySelector("#transactionsTable tbody");
    tableBody.innerHTML = "";

    try {
        const res = await fetch(`${API_BASE}/api/accounts/${accountId}/transactions`);

        if (!res.ok) {
            alert("Errore nel caricamento delle transazioni (conto non trovato?)");
            return;
        }

        const data = await res.json();

        data.forEach(tx => {
            const amount = Number(tx.amount);
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${tx.id}</td>
                <td>${tx.type}</td>
                <td>${amount.toFixed(2)}</td>
                <td>${tx.currency}</td>
                <td>${tx.description}</td>
                <td>${new Date(tx.created_at).toLocaleString()}</td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        alert("Errore di rete nel caricamento delle transazioni");
    }
}

async function submitTransfer(event) {
    event.preventDefault();

    const sourceAccountId = Number(document.getElementById("sourceAccountId").value);
    const targetAccountId = Number(document.getElementById("targetAccountId").value);
    const amount = Number(document.getElementById("amount").value);
    const feedbackDiv = document.getElementById("transferResult");

    feedbackDiv.textContent = "";
    feedbackDiv.className = "feedback";

    if (!sourceAccountId || !targetAccountId || !amount) {
        feedbackDiv.textContent = "Compila tutti i campi del trasferimento";
        feedbackDiv.classList.add("error");
        return;
    }

    const payload = {
        source_account_id: sourceAccountId,
        target_account_id: targetAccountId,
        amount: amount
    };

    try {
        const res = await fetch(`${API_BASE}/api/transfers`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const body = await res.json();

        if (!res.ok) {
            feedbackDiv.textContent = `Errore: ${body.detail || "Trasferimento fallito"}`;
            feedbackDiv.classList.add("error");
            return;
        }

        // Successo
        feedbackDiv.textContent =
            `Trasferimento riuscito! Nuovo saldo conto sorgente: ${body.new_source_balance.toFixed(2)}, ` +
            `conto destinazione: ${body.new_target_balance.toFixed(2)} (importo accreditato: ${body.credited_amount.toFixed(2)}).`;
        feedbackDiv.classList.add("success");

        // Aggiorna conti e transazioni
        await loadAccounts();
        // Se uno dei due conti è selezionato, aggiorno eventuali transazioni viste
        const selectedAccount = document.getElementById("accountSelect").value;
        if (selectedAccount) {
            await loadTransactions();
        }
    } catch (err) {
        console.error(err);
        feedbackDiv.textContent = "Errore di rete durante il trasferimento";
        feedbackDiv.classList.add("error");
    }
}

// Collego i bottoni agli handler quando il DOM è pronto
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("loadAccountsBtn").addEventListener("click", loadAccounts);
    document.getElementById("loadTransactionsBtn").addEventListener("click", loadTransactions);
    document.getElementById("transferForm").addEventListener("submit", submitTransfer);
});
