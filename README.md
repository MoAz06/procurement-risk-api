# Procurement Risk API

A backend/data engineering project that ingests invoice data from CSV, stores it in PostgreSQL, detects procurement risk signals, and exposes the results through a FastAPI API.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn

## Features

- CSV ingestion pipeline
- PostgreSQL-backed API
- Risk detection:
  - Duplicate invoices
  - Amount below threshold
  - Weekend invoices
- Filtering by amount and severity
- Analytics summary endpoint

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/invoices` | Get invoices |
| GET | `/risk-signals` | Get risk signals |
| GET | `/analytics/summary` | Get summary metrics |
| POST | `/pipeline/run` | Load CSV data into PostgreSQL |

## Setup

```bash
git clone git@github.com:MoAz06/procurement-risk-api.git
cd procurement-risk-api

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a PostgreSQL database:

```sql
CREATE DATABASE procurement_db;
```

Create a `.env` file in the project root:

```text
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/procurement_db
```

Load the environment variables and initialize the database:

```bash
export $(cat .env | xargs)
python -m app.init_db
```

Start the API:

```bash
uvicorn app.main:app --reload
```

## Usage

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Run the pipeline first:

```text
POST /pipeline/run
```

Then test:

```text
GET /invoices
GET /risk-signals
GET /analytics/summary
```

## Pipeline Flow

```text
CSV → PostgreSQL → FastAPI → Risk signals / analytics
```

## API Screenshot

![API Docs](docs/screenshot.png)

## Notes

The API reads invoice data from PostgreSQL. The CSV file is only used as the ingestion source through `/pipeline/run`.

Local secrets are stored in `.env` and should not be committed.
