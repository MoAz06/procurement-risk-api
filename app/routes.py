from fastapi import APIRouter
from pipeline.ingest import load_invoices
from pipeline.rules import detect_amount_below_threshold, detect_duplicate_invoices

router = APIRouter()


@router.get("/invoices")
def get_invoices():
    return load_invoices("data/invoices.csv")


@router.get("/risk-signals")
def get_risk_signals():
    invoices = load_invoices("data/invoices.csv")

    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))

    return risks


@router.get("/analytics/summary")
def get_summary():
    invoices = load_invoices("data/invoices.csv")

    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))

    total_invoices = len(invoices)
    total_risks = len(risks)
    high_risks = len([r for r in risks if r["severity"] == "high"])

    return {
        "total_invoices": total_invoices,
        "total_risk_signals": total_risks,
        "high_risk_signals": high_risks
    }