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