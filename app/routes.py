from fastapi import APIRouter, Query
from pipeline.ingest import load_invoices
from pipeline.rules import (
    detect_amount_below_threshold,
    detect_duplicate_invoices,
    detect_weekend_invoices
)

router = APIRouter()


@router.get("/invoices")
def get_invoices(min_amount: float = None):
    invoices = load_invoices("data/invoices.csv")

    if min_amount:
        invoices = [i for i in invoices if i["amount"] >= min_amount]

    return invoices


@router.get("/risk-signals")
def get_risk_signals(severity: str = None):
    invoices = load_invoices("data/invoices.csv")

    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))
    risks.extend(detect_weekend_invoices(invoices))

    if severity:
        risks = [r for r in risks if r["severity"] == severity]

    return risks

@router.get("/analytics/summary")
def get_summary():
    invoices = load_invoices("data/invoices.csv")

    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))
    risks.extend(detect_weekend_invoices(invoices))

    total_invoices = len(invoices)
    total_risks = len(risks)
    high_risks = len([r for r in risks if r["severity"] == "high"])

    return {
        "total_invoices": total_invoices,
        "total_risk_signals": total_risks,
        "high_risk_signals": high_risks
    }

@router.post("/pipeline/run")
def run_pipeline():
    invoices = load_invoices("data/invoices.csv")

    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))
    risks.extend(detect_weekend_invoices(invoices))

    return {
        "status": "pipeline executed",
        "invoices_processed": len(invoices),
        "risks_found": len(risks)
    }