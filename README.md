# Procurement Risk API

A backend/data project that processes invoice data from CSV files, detects risk signals, and exposes results via a FastAPI API.

## Features
- CSV ingestion
- Risk detection:
  - Duplicate invoices
  - Amount below threshold
  - Weekend invoices
- Filtering (e.g. severity)
- Pipeline trigger endpoint

## Endpoints
- GET /invoices
- GET /risk-signals
- GET /analytics/summary
- POST /pipeline/run

## Run locally
```bash
uvicorn app.main:app --reload
