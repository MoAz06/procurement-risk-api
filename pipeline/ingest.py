from app.database import SessionLocal
from app.models import Invoice
import csv

def save_invoices_to_db(invoices):
    db = SessionLocal()

    existing_ids = {
        i.invoice_id for i in db.query(Invoice.invoice_id).all()
    }

    for inv in invoices:
        if inv["invoice_id"] in existing_ids:
            continue  # skip duplicates

        db_invoice = Invoice(
            invoice_id=inv["invoice_id"],
            supplier=inv["supplier"],
            amount=inv["amount"],
            status=inv["status"],
            invoice_date=inv["invoice_date"]
        )

        db.add(db_invoice)

    db.commit()
    db.close()

    
def load_invoices(path):
    invoices = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            invoices.append({
                "invoice_id": int(row["invoice_id"]),
                "supplier": row["supplier"],
                "amount": float(row["amount"]),
                "status": row["status"],
                "invoice_date": row["invoice_date"]
            })

    return invoices


def save_invoices_to_db(invoices):
    db = SessionLocal()

    for inv in invoices:
        db_invoice = Invoice(
            invoice_id=inv["invoice_id"],
            supplier=inv["supplier"],
            amount=inv["amount"],
            status=inv["status"],
            invoice_date=inv["invoice_date"]
        )

        db.add(db_invoice)

    db.commit()
    db.close()