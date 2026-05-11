from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Order
from app.database.models import Product

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    notifications = []

    orders = db.query(Order).all()
    products = db.query(Product).all()

    for order in orders:
        if order.status == "Delayed":
            notifications.append({
                "type": "warning",
                "message": f"Order #{order.id} is delayed"
            })

    for product in products:
        if product.stock <= product.critical_stock:
            notifications.append({
                "type": "critical",
                "message": f"{product.name} stock is critically low"
            })

    return notifications