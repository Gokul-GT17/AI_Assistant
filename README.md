# AI Assistant for Customer Support Tickets

A lightweight AI system for analyzing support tickets, answering natural language questions, and detecting ticket anomalies.

## Features

- Ask questions about support ticket data
- Detect unresolved high-priority tickets
- Identify unusually long ticket resolution times
- Serve results via FastAPI
- Provide a Streamlit dashboard for interaction

## Files

- `app.py` — FastAPI server with `/ask` and `/anomalies`
- `query_engine.py` — LLM prompt builder and Groq integration
- `anomaly_detection.py` — CSV-based anomaly detection logic
- `streamlit_ui.py` — Streamlit user interface
- `support_tickets.csv` — Ticket dataset
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (not committed)

## Requirements

- Python 3.10+
- `pip`
- Groq API key
- `support_tickets.csv` present in the project root

## Quick Start

1. Create and activate a Python virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your Groq API key to `.env`:
```env
GROQ_API_KEY=your_groq_api_key
```

4. Make sure `support_tickets.csv` is in the repository root.

## Run the Project

Start the API server:
```bash
uvicorn app:app --reload
```

Then start the Streamlit UI in a second terminal:
```bash
streamlit run streamlit_ui.py
```

Visit the UI at `http://localhost:8501`.

## API Endpoints

- `GET /` — health check
- `POST /ask` — question answering
  - Request: `{ "question": "..." }`
  - Response: `{ "question": "...", "answer": "..." }`
- `GET /anomalies` — list detected ticket anomalies

## How It Works

- `query_engine.py` reads `support_tickets.csv` and sends a dataset-aware prompt to Groq.
- `anomaly_detection.py` flags tickets that are high-priority and unresolved or have long resolution times.
- `app.py` exposes the functionality as REST endpoints.
- `streamlit_ui.py` provides a simple browser interface for asking questions and viewing anomalies.

## Notes

- The Streamlit UI depends on the FastAPI server running locally.
- If you change the dataset filename, update the code references in `query_engine.py` and `anomaly_detection.py`.
- The current model configured in `query_engine.py` is `llama-3.3-70b-versatile`.


## Environment Management

### Python Dotenv

Used for secure API key management.

---

# Example Queries with Outputs

## Query 1

### Input

```text
How many tickets are currently open?
```

### Output

```text
To find the number of tickets that are currently open, we need to look at the 'status' column in the dataset.

There are 3 tickets with the status 'Open':

TKT-005
TKT-007
TKT-010
Therefore, the answer is 3. There are 3 tickets that are currently open.
```

---

## Query 2

### Input

```text
Which agent resolved the most tickets this month?
```

### Output

```text
The agent who resolved the most tickets this month is AGT-07 with 1 tickets.
```

---

## Query 3

### Input

```text
Show me all Critical tickets not resolved within 12 hours
```

### Output

```text
This output shows that there is only one Critical ticket (TKT-004) that was not resolved within 12 hours.

```

---

## Query 4

### Input

```text
What is the average customer rating for Technical category tickets?
```

### Output

```text
To find the average customer rating for Technical category tickets, we need to filter the data for Technical category and then calculate the average of the customer_rating column.

Based on the provided dataset, there are two tickets in the Technical category: TKT-006 and TKT-010. However, TKT-010 has a NaN (Not a Number) value for customer_rating since its status is Open, implying that the customer has not yet rated the support.

For TKT-006, the customer_rating is 2.0.

Since there is only one ticket with a valid customer_rating, the average customer rating for Technical category tickets is 2.0.
```

---

## Query 5

### Input

```text
Are there any anomalies in resolution times this week?
```

### Output

```text
There are no anomalies in resolution times this week.
```

---

# Anomaly Detection Logic

## Rule 1: High-Priority Unresolved Tickets

A ticket is flagged if:

```text
Priority = High or Critical
AND
Status != Resolved
```

---

## Rule 2: Long Resolution Time

A ticket is flagged if:

```text
Resolution Time >
Mean Resolution Time + (2 × Standard Deviation)
```

This identifies unusually slow ticket resolutions.

---

# Known Limitations

### 1. Limited Dataset Context

The LLM receives dataset schema and sample records rather than the complete dataset. Answers may not always reflect exact dataset-wide statistics.

### 2. No SQL Query Engine

The current implementation does not translate natural language questions into executable SQL or Pandas queries.

### 3. Rule-Based Anomaly Detection

Anomalies are identified using predefined statistical thresholds and business rules rather than machine learning models.

### 4. No Authentication

The API currently does not implement authentication or authorization mechanisms.

### 5. CSV-Based Storage

The solution operates on CSV files and does not support relational databases or data warehouses.

### 6. Scalability Constraints

Large datasets may increase response latency due to repeated CSV loading and processing.

# Conclusion

This project demonstrates how Generative AI can be combined with customer support ticket data to enable intelligent querying, anomaly detection, and operational analytics through a lightweight and scalable architecture built with Groq, FastAPI, Streamlit, and Pandas.
