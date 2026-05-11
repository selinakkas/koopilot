from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return [
        {
            "id": order.id,
            "customer": order.customer,
            "product": order.product,
            "quantity": order.quantity,
            "status": order.status,
            "cargo_id": order.cargo_id,
        }
        for order in orders
    ]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "customer": order.customer,
        "product": order.product,
        "quantity": order.quantity,
        "status": order.status,
        "cargo_id": order.cargo_id,
    }