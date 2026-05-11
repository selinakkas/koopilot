from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Order
from app.database.models import Product

from io import BytesIO
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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


@router.get("/daily/pdf")
def generate_daily_report_pdf(db: Session = Depends(get_db)):
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

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "KOOPILOT DAILY OPERATIONS REPORT")

    y -= 40
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total Orders: {len(orders)}")
    y -= 20
    pdf.drawString(50, y, f"Delayed Orders: {len(delayed_orders)}")
    y -= 20
    pdf.drawString(50, y, f"Critical Stock Products: {len(critical_products)}")

    y -= 40
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Delayed Orders")

    y -= 25
    pdf.setFont("Helvetica", 10)

    if delayed_orders:
        for order in delayed_orders:
            pdf.drawString(
                50,
                y,
                f"- Order #{order.id} | {order.customer} | {order.product}"
            )
            y -= 18
    else:
        pdf.drawString(50, y, "- No delayed orders")
        y -= 18

    y -= 25
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Critical Stock Products")

    y -= 25
    pdf.setFont("Helvetica", 10)

    if critical_products:
        for product in critical_products:
            pdf.drawString(
                50,
                y,
                f"- {product.name} | Stock: {product.stock} | Critical Level: {product.critical_stock}"
            )
            y -= 18
    else:
        pdf.drawString(50, y, "- No critical stock products")
        y -= 18

    y -= 25
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Recommended Actions")

    y -= 25
    pdf.setFont("Helvetica", 10)
    actions = [
        "Follow up with delayed shipments.",
        "Restock critical products.",
        "Monitor products close to critical stock level.",
    ]

    for action in actions:
        pdf.drawString(50, y, f"- {action}")
        y -= 18

    pdf.save()

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=koopilot-daily-report.pdf"
        }
    )