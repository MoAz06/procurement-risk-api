from fastapi import APIRouter
from pipeline.ingest import load_invoices
from pipeline.rules import detect_amount_below_threshold

router = APIRouter()


@router.get("/invoices")
def get_invoices():
    return load_invoices("data/invoices.csv")


@router.get("/risk-signals")
def get_risk_signals():
    return [
        {
            "risk_id": 1,
            "invoice_id": 1,
            "type": "amount_below_threshold",
            "severity": "medium"
        }
    ]


@router.get("/analytics/summary")
def get_summary():
    return {
        "total_invoices": 2,
        "total_risk_signals": 1,
        "high_risk_signals": 0
    }


@router.get("/risk-signals")
def get_risk_signals():
    invoices = load_invoices("data/invoices.csv")
    risks = detect_amount_below_threshold(invoices)
    return risks