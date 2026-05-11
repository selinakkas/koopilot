import json
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_service import generate_ai_response

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
    orders = load_json("orders.json")
    products = load_json("products.json")
    cargos = load_json("cargos.json")

    context = {
        "orders": orders,
        "products": products,
        "cargos": cargos,
    }

    try:
        ai_answer = generate_ai_response(request.message, context)
        return {"answer": ai_answer}
    except Exception:
        pass

    message = request.message.lower()