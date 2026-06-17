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
Example Queries
Query 1

Input

How many tickets are currently open?

Output

To find the number of tickets that are currently open, we need to look at the 'status' column in the dataset.

There are 3 tickets with the status 'Open':

TKT-005
TKT-007
TKT-010
Therefore, the answer is 3. There are 3 tickets that are currently open.
Query 2

Input

Which agent resolved the most tickets this month?

Output

Based on the sample data, the agent who resolved the most tickets this month is AGT-07 and AGT-06 and AGT-09, they all resolved one ticket each.
Query 3

Input

Show me all Critical tickets not resolved within 12 hours.

Output

  ticket_id       created_at category priority    status  response_time_hrs  resolution_time_hrs agent_id  customer_rating                             issue_summary
3   TKT-004  2024-03-09 09:59    Billing     High  Resolved                0.6                 10.7   AGT-07              4.0  Subscription not activated after payment

 There is only one Critical (High) ticket that was resolved but took more than 12 hours to resolve.
Query 4

Input

What is the average customer rating for Technical category tickets?

Output

To calculate the average customer rating for Technical category tickets, we need to filter the data for the Technical category and then calculate the mean of the customer_rating column.

Based on the provided dataset, there are two tickets in the Technical category: TKT-006 and TKT-010. However, TKT-010 is still open and does not have a customer rating.

For TKT-006, the customer rating is 2.0.

Since there is only one ticket with a customer rating in the Technical category, the average customer rating is 2.0.

Query 5

Input
Are there any anomalies in resolution times this week?

Output
There is one anomaly in resolution times this week, which is ticket TKT-006 with a resolution time of 34.1 hours. This is significantly higher than the mean resolution time for the week.

Please note that this analysis is based on the assumption that the dataset is representative of the population and that the current week is the week ending on '2024-03-25'. The actual anomalies may vary depending on the current date and the actual dataset.


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
