from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Order
from app.database.models import Product
from app.database.models import Shipment

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    products = db.query(Product).all()
    shipments = db.query(Shipment).all()

    delayed_shipments = [
        shipment for shipment in shipments
        if shipment.status == "Delayed"
    ]

    critical_products = [
        product for product in products
        if product.stock <= product.critical_stock
    ]

    return {
        "total_orders": len(orders),
        "delayed_shipments": len(delayed_shipments),
        "critical_products": len(critical_products),
        "daily_summary": (
            f"There are {len(delayed_shipments)} delayed shipments "
            f"and {len(critical_products)} products at critical stock level."
        )
    }


@router.get("/ai-summary")
def get_ai_operation_summary(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    products = db.query(Product).all()
    shipments = db.query(Shipment).all()

    delayed_cargo_ids = [
        shipment.cargo_id for shipment in shipments
        if shipment.status.lower() == "delayed"
    ]

    delayed_orders = [
        order for order in orders
        if order.cargo_id in delayed_cargo_ids
    ]

    critical_products = [
        product for product in products
        if product.stock <= product.critical_stock
    ]

    summary = (
        f"Today, Koopilot detected {len(delayed_orders)} delayed order(s) "
        f"and {len(critical_products)} product(s) at critical stock level. "
    )

    if critical_products:
        product_names = ", ".join(
            [product.name for product in critical_products]
        )
        summary += f"Low-stock products: {product_names}. "

    if delayed_orders:
        order_ids = ", ".join(
            [f"#{order.id}" for order in delayed_orders]
        )
        summary += f"Delayed orders: {order_ids}. "

    summary += (
        "The operations team should prioritize stock replenishment "
        "and shipment follow-up."
    )

    return {"summary": summary}


@router.get("/action-plan")
def get_daily_action_plan(db: Session = Depends(get_db)):
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

    actions = []

    if delayed_orders:
        actions.append({
            "priority": "High",
            "action": f"Follow up with {len(delayed_orders)} delayed order(s)."
        })

    if critical_products:
        actions.append({
            "priority": "High",
            "action": f"Restock {len(critical_products)} critical product(s)."
        })

    actions.append({
        "priority": "Medium",
        "action": "Review customer complaint risks and AI assistant recommendations."
    })

    actions.append({
        "priority": "Low",
        "action": "Monitor healthy stock items and upcoming shipments."
    })

    return actions