# Procurement Risk API

A backend/data project that processes invoice data from CSV files, detects risk signals, and exposes results via a FastAPI API.

## Features
- CSV data ingestion
- Risk detection (duplicate invoices, threshold, weekend)
- REST API with FastAPI
- Filtering endpoints

## Endpoints
- GET /invoices
- GET /risk-signals
- GET /analytics/summary
- POST /pipeline/run

## Run locally
```bash
uvicorn app.main:app --reload# procurement-risk-api
