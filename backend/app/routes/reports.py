from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Order
from app.database.models import Product

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/daily", response_class=PlainTextResponse)
def generate_daily_report(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    products = db.query(Product).all()

    delayed_orders = [
        order for order in orders
        if order.status == "Delayed"
    ]

    critical_products = [
        product for product in products
        if product.stock <= product.critical_stock
    ]

    report = f"""
KOOPILOT DAILY OPERATIONS REPORT

Overview
- Total Orders: {len(orders)}
- Delayed Orders: {len(delayed_orders)}
- Critical Stock Products: {len(critical_products)}

Delayed Orders
{chr(10).join([f"- Order #{order.id} | Customer: {order.customer} | Product: {order.product}" for order in delayed_orders]) or "- No delayed orders"}

Critical Stock Products
{chr(10).join([f"- {product.name} | Stock: {product.stock} | Critical Level: {product.critical_stock}" for product in critical_products]) or "- No critical stock products"}

Recommended Actions
- Follow up with delayed shipments.
- Restock critical products.
- Monitor products close to critical stock level.
"""

    return report