# Procurement Risk API

A production-style backend/data engineering project that ingests invoice data from CSV, stores it in PostgreSQL, detects procurement risk signals, and exposes secured endpoints via a FastAPI API.

## Tech Stack

- Python  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Uvicorn  
- JWT (authentication)  
- Passlib (bcrypt)

## Features

- CSV ingestion pipeline  
- PostgreSQL-backed API  
- JWT authentication (login/register)  
- Protected routes (Bearer token)  
- Password hashing (bcrypt)  

### Risk Detection
- Duplicate invoices  
- Amount below threshold  
- Weekend invoices  

### API Capabilities
- Filtering by amount and severity  
- Analytics summary endpoint  

## Endpoints

### Public
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Login (returns JWT) |

### Protected (Bearer Token Required)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/invoices` | Get invoices |
| GET | `/risk-signals` | Get risk signals |
| GET | `/analytics/summary` | Get summary metrics |
| POST | `/pipeline/run` | Load CSV data |

## Authentication

Login returns a JWT token:

POST /auth/login

Use the token in requests:

Authorization: Bearer <your_token>

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

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/procurement_db  
SECRET_KEY=your_random_secret_key

Load environment variables and initialize the database:

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

http://127.0.0.1:8000/docs

Run the pipeline first:

POST /pipeline/run

Then test:

GET /invoices  
GET /risk-signals  
GET /analytics/summary  

## Pipeline Flow

CSV → PostgreSQL → FastAPI → Risk signals / analytics

## API Screenshot

![API Docs](docs/screenshot.png)

## Notes

- The API reads invoice data from PostgreSQL  
- The CSV file is only used as ingestion input via `/pipeline/run`  
- Secrets are stored in `.env` and must not be committed  
