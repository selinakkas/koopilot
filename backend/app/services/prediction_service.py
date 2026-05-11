def generate_predictions(products):
    predictions = []

    for product in products:
        remaining_ratio = (
            product.stock / product.critical_stock
        )

        if remaining_ratio <= 1:
            predictions.append({
                "type": "critical",
                "message": f"{product.name} stock may run out very soon."
            })

        elif remaining_ratio <= 2:
            predictions.append({
                "type": "warning",
                "message": f"{product.name} inventory should be monitored closely."
            })

    return predictions