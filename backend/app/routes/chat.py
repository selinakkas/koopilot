import json
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["AI Chat"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class ChatRequest(BaseModel):
    message: str


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def find_order_by_id(message: str):
    orders = load_json("orders.json")
    cargos = load_json("cargos.json")

    for order in orders:
        if str(order["id"]) in message:
            cargo = next(
                (c for c in cargos if c["cargo_id"] == order["cargo_id"]),
                None
            )

            return {
                "order": order,
                "cargo": cargo
            }

    return None


def get_critical_stock_answer():
    products = load_json("products.json")

    critical_products = [
        product for product in products
        if product["stock"] <= product["critical_stock"]
    ]

    if not critical_products:
        return "There are currently no products at critical stock level."

    product_names = ", ".join(
        [f"{p['name']} ({p['stock']} units left)" for p in critical_products]
    )

    return f"Products at critical stock level: {product_names}."


def get_delayed_orders_answer():
    orders = load_json("orders.json")
    cargos = load_json("cargos.json")

    delayed_cargo_ids = [
        cargo["cargo_id"] for cargo in cargos
        if cargo["status"].lower() == "delayed"
    ]

    delayed_orders = [
        order for order in orders
        if order["cargo_id"] in delayed_cargo_ids
    ]

    if not delayed_orders:
        return "There are no delayed orders today."

    order_ids = ", ".join([f"#{order['id']}" for order in delayed_orders])
    return f"Orders with delivery delays: {order_ids}."


@router.post("/")
def chat(request: ChatRequest):
    message = request.message.lower()

    order_result = find_order_by_id(message)

    if order_result:
        order = order_result["order"]
        cargo = order_result["cargo"]

        cargo_status = cargo["status"] if cargo else "Unknown"
        estimated_delivery = cargo.get("estimated_delivery", "Unknown") if cargo else "Unknown"

        return {
            "answer": (
                f"Order #{order['id']} is currently {order['status']}. "
                f"Cargo status: {cargo_status}. "
                f"Estimated delivery: {estimated_delivery}."
            )
        }

    if "stock" in message or "inventory" in message or "low" in message:
        return {"answer": get_critical_stock_answer()}

    if "delayed" in message or "delay" in message or "cargo" in message or "shipment" in message:
        return {"answer": get_delayed_orders_answer()}

    return {
        "answer": (
            "You can ask me about orders, stock levels, or shipments. "
            "For example: 'Where is order 128?'"
        )
    }