import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/summary")
def get_dashboard_summary():
    orders = load_json("orders.json")
    products = load_json("products.json")
    cargos = load_json("cargos.json")

    total_orders = len(orders)

    delayed_orders = [
        cargo for cargo in cargos
        if cargo["status"] == "Delayed"
    ]

    critical_products = [
        product for product in products
        if product["stock"] <= product["critical_stock"]
    ]

    return {
        "total_orders": total_orders,
        "delayed_shipments": len(delayed_orders),
        "critical_products": len(critical_products),
        "daily_summary": (
            f"There are {len(delayed_orders)} delayed shipments "
            f"and {len(critical_products)} products at critical stock level."
        )
    }

@router.get("/ai-summary")
def get_ai_operation_summary():
    orders = load_json("orders.json")
    products = load_json("products.json")
    cargos = load_json("cargos.json")

    delayed_cargo_ids = [
        cargo["cargo_id"] for cargo in cargos
        if cargo["status"].lower() == "delayed"
    ]

    delayed_orders = [
        order for order in orders
        if order["cargo_id"] in delayed_cargo_ids
    ]

    critical_products = [
        product for product in products
        if product["stock"] <= product["critical_stock"]
    ]

    summary = (
        f"Today, Koopilot detected {len(delayed_orders)} delayed order(s) "
        f"and {len(critical_products)} product(s) at critical stock level. "
    )

    if critical_products:
        product_names = ", ".join([p["name"] for p in critical_products])
        summary += f"Low-stock products: {product_names}. "

    if delayed_orders:
        order_ids = ", ".join([f"#{o['id']}" for o in delayed_orders])
        summary += f"Delayed orders: {order_ids}. "

    summary += "The operations team should prioritize stock replenishment and shipment follow-up."

    return {"summary": summary}