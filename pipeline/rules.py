def detect_amount_below_threshold(invoices, threshold=5000):
    risks = []

    for invoice in invoices:
        amount = invoice["amount"]

        # check: net onder threshold (bijv 4950 bij 5000)
        if threshold - 100 <= amount < threshold:
            risks.append({
                "invoice_id": invoice["invoice_id"],
                "type": "amount_below_threshold",
                "severity": "medium"
            })

    return risks