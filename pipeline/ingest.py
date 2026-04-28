import csv

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