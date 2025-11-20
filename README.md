# project-work-indelicato-
Progetto Revolut
Dashboard Multivaluta – Prototipo stile Revolut
Applicazione full-stack API-based sviluppata come project work universitario.
Backend realizzato con FastAPI, frontend in HTML/CSS/JavaScript, database simulato in memoria.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Questa Web App permette di:
-Visualizzare i conti associati a un utente
-Visualizzare le transazioni di un conto
-Effettuare un trasferimento interno tra due conti

Gestire automaticamente:
-tasso di cambio EUR ↔ USD
-aggiornamento dei saldi
-creazione di nuove transazioni
-Utilizzare un backend moderno RESTful con FastAPI
-Simulare un ambiente fintech tipo Revolut
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Tecnologie
Frontend: HTML5, CSS3, JavaScript (Vanilla)
Backend: Python 3, FastAPI, Uvicorn (server ASGI)

Database:
Simulato in memoria tramite dizionari Python
(User, Account, Transaction)

Struttura del progetto:
project-work-indelicato-/
│ index.html
│ styles.css
│ app.js
│ main.py
│ models.py
│ database.py
│ services.py
│ README.md
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installazione:
1. Clona la repo
git clone <URL-repository>
cd <nome-cartella>

2. Crea ambiente virtuale
Windows:
python -m venv venv
venv\Scripts\activate

3. Installa le dipendenze
pip install fastapi uvicorn

Avvio del backend:
Nella cartella del progetto:
uvicorn main:app --reload

Se tutto ok vedrai:
Uvicorn running on http://127.0.0.1:8000

Avvio del frontend:
-Avvia un server statico
python -m http.server 5500


Poi visita:
http://127.0.0.1:5500/index.html

Documentazione API (Swagger):
FastAPI genera automaticamente la documentazione interattiva:
http://127.0.0.1:8000/docs
Puoi testare gli endpoint direttamente da lì.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Funzionamento dell’app:
1️⃣ Carica conti utente
Inserisci un user_id (es. 1) → clicca “Carica conti”
2️⃣ Visualizza le transazioni
Seleziona un conto → clicca “Carica transazioni”
3️⃣ Effettua un trasferimento
Compila il form:
ID conto sorgente
ID conto destinazione
Importo
→ clicca “Esegui trasferimento”

Il sistema: controlla i fondi disponibili, calcola il tasso di cambio, aggiorna i saldi, registra le nuove transazioni, aggiorna la dashboard.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🔌 Endpoint API
GET /api/users/{user_id}/accounts
Restituisce tutti i conti dell’utente.

GET /api/accounts/{account_id}/transactions
Restituisce le transazioni del conto.

POST /api/transfers
Esegue un trasferimento interno.

Body JSON esempio:

{
  "source_account_id": 101,
  "target_account_id": 102,
  "amount": 100
}

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Autore:
Indelicato Antonello
Project Work – Informatica per le Aziende Digitali (L-31)
