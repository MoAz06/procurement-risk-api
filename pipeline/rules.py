from datetime import datetime

def detect_amount_below_threshold(invoices, threshold=5000):
    risks = []

    for invoice in invoices:
        amount = invoice["amount"]

        if threshold - 100 <= amount < threshold:
            risks.append({
                "invoice_id": invoice["invoice_id"],
                "type": "amount_below_threshold",
                "severity": "medium"
            })

    return risks


def detect_duplicate_invoices(invoices):
    risks = []
    seen = {}

    for invoice in invoices:
        key = (invoice["supplier"], invoice["amount"])

        if key in seen:
            risks.append({
                "invoice_id": invoice["invoice_id"],
                "type": "duplicate_invoice",
                "severity": "high"
            })
        else:
            seen[key] = invoice["invoice_id"]

    return risks



def detect_weekend_invoices(invoices):
    risks = []

    for invoice in invoices:
        invoice_date = datetime.strptime(invoice["invoice_date"], "%Y-%m-%d")

        if invoice_date.weekday() >= 5:
            risks.append({
                "invoice_id": invoice["invoice_id"],
                "type": "weekend_invoice",
                "severity": "low"
            })

    return risks