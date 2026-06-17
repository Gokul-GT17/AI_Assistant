# AI Assistant — Support Ticket QA & Anomaly Detection

Lightweight assistant for analyzing support tickets (CSV), answering natural-language questions via Groq LLM, and detecting simple rule-based anomalies.

## Quick summary

- Backend: `app.py` (FastAPI)
- Query logic: `query_engine.py` (Groq client)
- Anomalies: `anomaly_detection.py` (CSV + Pandas rules)
- UI: `streamlit_ui.py` (Streamlit)
- Data: `support_tickets.csv`

## Requirements

- Python 3.10+
- pip
- `GROQ_API_KEY` set in a `.env` file

## Files

- `app.py` — exposes `/` (health), `/ask` (POST), and `/anomalies` (GET)
- `query_engine.py` — loads `support_tickets.csv`, builds a prompt and calls Groq (`llama-3.3-70b-versatile` by default)
- `anomaly_detection.py` — flags unresolved High/Critical tickets and long resolution times
- `streamlit_ui.py` — simple frontend that calls the API at `http://localhost:8000`
- `requirements.txt` — dependencies

## Setup

1. Create and activate a virtual environment

Windows
```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add `.env` with your Groq API key

```
GROQ_API_KEY=your_groq_api_key
```

4. Ensure `support_tickets.csv` is present in the project root.

## Run

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Start the Streamlit UI (in another terminal):

```bash
streamlit run streamlit_ui.py
```

Access the UI at http://localhost:8501 and the API at http://localhost:8000

## API (examples)

Health check

```bash
curl http://localhost:8000/
```

Ask a question

```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How many unresolved high priority tickets are there?"}'
```

Detect anomalies

```bash
curl http://localhost:8000/anomalies
```

Example anomalies response

```json
[ { "ticket_id": "123", "issue": "Unresolved high-priority ticket" } ]
```

## Expected CSV schema (minimum)

The code expects at least these columns in `support_tickets.csv`:

- `ticket_id` — unique identifier
- `priority` — values like `Low`, `Medium`, `High`, `Critical`
- `status` — e.g. `Open`, `In Progress`, `Resolved`
- `resolution_time_hrs` — numeric, hours to resolve (may be blank)

Example single-row CSV (header + row):

```csv
ticket_id,priority,status,resolution_time_hrs
TKT-001,High,Open,
```

## Anomaly rules (implemented)

- Unresolved high-priority tickets: `priority` in [`High`, `Critical`] and `status` != `Resolved`.
- Long resolution times: `resolution_time_hrs` > mean + 2*std (computed over non-null values).

## Implementation notes

- `query_engine.py` reads the dataset and includes sample rows in the prompt sent to Groq. The model used and temperature are set there.
- `streamlit_ui.py` uses `API_URL = "http://localhost:8000"`. Change this if the API runs elsewhere.
- No authentication is implemented; do not expose this server publicly without adding auth and rate limits.

## Troubleshooting

- If Streamlit shows connection errors, ensure the FastAPI server is running and `API_URL` matches the server address.
- If Groq authentication fails, verify `GROQ_API_KEY` in `.env` and restart the server.
- For large CSVs, consider sampling or adding pagination in the query prompt to avoid very long prompts.

---

Want a sample `support_tickets.csv` file, pinned `requirements.txt` versions, or a tiny test script to exercise the API? Tell me which and I'll add it.
