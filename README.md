# AI Assistant for Ticket Support

## Overview

AI Assistant for Ticket Support is a Generative AI-powered ticket analytics system that enables users to query customer support ticket data using natural language and automatically detect anomalies in ticket resolution patterns.

The system combines FastAPI, Streamlit, Pandas, LangChain, Groq LLM, and a Pandas DataFrame Agent to provide intelligent insights from support ticket datasets without requiring SQL knowledge.

---
# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
cd project
```

---

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Obtain an API key from Groq.

---

## 5. Run FastAPI Backend

```bash
uvicorn app:app --reload
```

Backend URL:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## 6. Run Streamlit Frontend

```bash
streamlit run streamlit_ui.py
```

---


## Features

### Natural Language Querying

Ask questions about support tickets in plain English, such as:

* How many critical tickets are unresolved?
* Which agent resolved the most tickets?
* What is the average customer satisfaction rating?
* Show all high-priority unresolved tickets.

### AI-Powered Analytics

Uses Groq-hosted Llama 3.3 70B model through LangChain to analyze ticket data and generate human-readable responses.

### Anomaly Detection

Automatically identifies:

* Tickets with unusually long resolution times
* Outlier tickets based on statistical thresholds

### REST API Support

Provides FastAPI endpoints for:

* Asking questions
* Retrieving anomaly reports

### Interactive Dashboard

Streamlit-based user interface for:

* Querying ticket data
* Viewing detected anomalies

---

# Architecture

```text
                    ┌─────────────────┐
                    │ Support Tickets │
                    │      CSV        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Data Loader   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Pandas DataFrame│
                    └───────┬─────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
┌──────────────────┐              ┌──────────────────┐
│  Query Engine    │              │ Anomaly Detector │
│ (LangChain Agent)│              │ Statistical Rule │
└────────┬─────────┘              └────────┬─────────┘
         │                                 │
         ▼                                 ▼
 ┌────────────────┐              ┌─────────────────┐
 │ Groq Llama 3.3 │              │ Anomaly Results │
 └────────────────┘              └─────────────────┘
                 │
                 ▼
          ┌─────────────┐
          │  FastAPI    │
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │ Streamlit UI│
          └─────────────┘
```

---

# Project Structure

```text
project/
│
├── app.py
├── data_loader.py
├── query_engine.py
├── anomaly_detector.py
├── requirements.txt
├── streamlit_ui.py
│
├── Data_set/
│   └── support_tickets.csv
│
└── .env
```

---

# Technology Stack

| Component              | Technology              |
| ---------------------- | ----------------------- |
| Backend API            | FastAPI                 |
| Frontend               | Streamlit               |
| Data Processing        | Pandas                  |
| LLM Provider           | Groq                    |
| LLM Model              | Llama 3.3 70B Versatile |
| AI Framework           | LangChain               |
| Environment Management | python-dotenv           |

---

# Model and Tools Used

## Large Language Model

**Model:** llama-3.3-70b-versatile

Used via Groq API for:

* Natural language understanding
* DataFrame reasoning
* Analytical responses

## LangChain Pandas Agent

The application uses:

```python
create_pandas_dataframe_agent()
```

This enables the LLM to:

* Inspect ticket data
* Execute DataFrame operations
* Answer analytical questions

## Statistical Anomaly Detection

Anomalies are detected using:

```python
threshold = mean + (2 × standard deviation)
```

Tickets exceeding this threshold are flagged as:

```text
Long Resolution Time
```

---


# API Endpoints

## Health Endpoint

```http
GET /
```

Response:

```json
{
  "message": "AI Assistant for Ticket Support"
}
```

---

## Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "Which agent resolved the most tickets?"
}
```

Response:

```json
{
  "question": "Which agent resolved the most tickets?",
  "answer": "Agent AGT-09 resolved the most tickets."
}
```

---

## Get Anomalies

```http
GET /anomalies
```

Response:

```json
{
  "count": 3,
  "anomalies": [
    {
      "ticket_id": "TKT-101",
      "type": "Long Resolution Time"
    }
  ]
}
```

---

# Example Queries

## Example 1

Question:

```text
How many tickets are currently open?
```

Output:

```text
There are 111 tickets that are currently open.
```

---

## Example 2

Question:

```text
Which agent resolved the most tickets this month?
```

Output:

```text
AGT-09 and AGT-12 resolved the most tickets, with 37 tickets each.
```

---

## Example 3

Question:

```text
Show me all Critical tickets not resolved within 12 hours
```

Output:

```text
There are 3 Critical tickets that were not resolved within 12 hours.
```

---

## Example 4

Question:

```text
What is the average customer rating for Technical category tickets?
```

Output:

```text
The average customer rating for Technical category tickets is 3.74.
```
## Example 5

Question:

```text
Are there any anomalies in resolution times this week?
```

Output:

```text
There are 2 anomalies in resolution times this week, with ticket IDs TKT-108 and TKT-130 having resolution times greater than 2 standard deviations above the mean.
```
---

# How Anomaly Detection Works

The anomaly detector:

1. Calculates mean resolution time.
2. Calculates standard deviation.
3. Creates a threshold:

```text
Threshold = Mean + (2 × Standard Deviation)
```

4. Flags tickets exceeding the threshold.
5. Returns ticket ID and anomaly type.

---

# Known Limitations

### Limited Anomaly Types

Currently detects only:

* Long resolution time outliers

Future versions can include:

* High-priority unresolved tickets
* SLA violations
* Reopened tickets
* Agent performance anomalies

### DataFrame Agent Dependency

Responses depend entirely on the provided dataset.

If information is not present in the CSV, the system returns:

```text
I cannot find this information in the ticket dataset.
```

### Memory Constraints

Large datasets may increase:

* Query latency
* Memory consumption

### CSV-Based Storage

Current version operates only on CSV files.

Database integration is not yet implemented.


---
# Summary

AI Assistant for Ticket Support is a Generative AI-powered analytics solution designed to simplify the exploration and analysis of customer support ticket data. By combining FastAPI, Streamlit, Pandas, LangChain, and Groq's Llama 3.3 model, the application enables users to interact with ticket datasets using natural language instead of traditional query languages.

The system supports intelligent ticket analysis through a conversational interface, allowing users to ask business-oriented questions such as ticket counts, agent performance metrics, resolution trends, and customer support insights. Additionally, it includes an anomaly detection module that automatically identifies tickets with unusually long resolution times using statistical analysis.

The solution demonstrates the practical application of Large Language Models (LLMs) for enterprise data analytics by transforming structured CSV data into an AI-driven question-answering system. Its modular architecture ensures easy extensibility for future enhancements such as advanced anomaly detection, vector search, Retrieval-Augmented Generation (RAG), real-time monitoring, and database integration.

This project showcases how Generative AI can improve operational visibility, reduce manual analysis efforts, and enable faster decision-making within customer support environments.




