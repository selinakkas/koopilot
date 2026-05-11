def calculate_order_risk(order, products):
    product = next(
        (
            p for p in products
            if p.name == order.product
        ),
        None
    )

    if order.status == "Delayed":
        return "HIGH"

    if product and product.stock <= product.critical_stock:
        return "HIGH"

    if product and product.stock <= product.critical_stock + 20:
        return "MEDIUM"

    return "LOW"