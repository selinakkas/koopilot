import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/orders", tags=["Orders"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_orders():
    with open(DATA_DIR / "orders.json", "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_orders():
    return load_orders()


@router.get("/{order_id}")
def get_order(order_id: int):
    orders = load_orders()

    for order in orders:
        if order["id"] == order_id:
            return order

    raise HTTPException(status_code=404, detail="Order not found")