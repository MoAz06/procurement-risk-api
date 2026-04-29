from fastapi import APIRouter, Depends
from app.database import SessionLocal
from app.models import Invoice, User
from app.auth import get_current_user
from pipeline.ingest import load_invoices, save_invoices_to_db
from pipeline.rules import (
    detect_amount_below_threshold,
    detect_duplicate_invoices,
    detect_weekend_invoices
)

router = APIRouter()


def invoices_to_dict(invoices_db):
    return [
        {
            "invoice_id": i.invoice_id,
            "supplier": i.supplier,
            "amount": i.amount,
            "status": i.status,
            "invoice_date": i.invoice_date
        }
        for i in invoices_db
    ]


def get_risks(invoices):
    risks = []
    risks.extend(detect_amount_below_threshold(invoices))
    risks.extend(detect_duplicate_invoices(invoices))
    risks.extend(detect_weekend_invoices(invoices))
    return risks


@router.get("/invoices")
def get_invoices(
    min_amount: float = None,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    query = db.query(Invoice)

    if min_amount is not None:
        query = query.filter(Invoice.amount >= min_amount)

    invoices_db = query.all()
    result = invoices_to_dict(invoices_db)

    db.close()
    return result


@router.get("/risk-signals")
def get_risk_signals(
    severity: str = None,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    invoices_db = db.query(Invoice).all()
    invoices = invoices_to_dict(invoices_db)

    db.close()

    risks = get_risks(invoices)

    if severity:
        risks = [r for r in risks if r["severity"] == severity]

    return risks


@router.get("/analytics/summary")
def get_summary(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    invoices_db = db.query(Invoice).all()
    invoices = invoices_to_dict(invoices_db)

    db.close()

    risks = get_risks(invoices)

    return {
        "total_invoices": len(invoices),
        "total_risk_signals": len(risks),
        "high_risk_signals": sum(1 for r in risks if r["severity"] == "high")
    }


@router.post("/pipeline/run")
def run_pipeline(
    current_user: User = Depends(get_current_user)
):
    invoices = load_invoices("data/invoices.csv")
    save_invoices_to_db(invoices)

    risks = get_risks(invoices)

    return {
        "status": "pipeline executed",
        "invoices_processed": len(invoices),
        "risks_found": len(risks)
    }