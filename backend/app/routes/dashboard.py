from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
from datetime import datetime

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


@router.get("/report")
def download_report(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    products = db.query(Product).all()
    shipments = db.query(Shipment).all()

    delayed_orders = [o for o in orders if o.status == "Delayed"]
    critical_products = [p for p in products if p.stock <= p.critical_stock]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title="Koopilot Daily Report", author="Koopilot")
    styles = getSampleStyleSheet()
    story = []

    # Başlık
    title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=24, textColor=colors.HexColor("#020617"), spaceAfter=6)
    sub_style = ParagraphStyle("sub", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#64748b"), spaceAfter=20)

    story.append(Paragraph("Koopilot Daily Report", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y – %H:%M')}", sub_style))
    story.append(Spacer(1, 0.5*cm))

    # Özet istatistikler
    story.append(Paragraph("Summary", styles["Heading2"]))
    summary_data = [
        ["Metric", "Value"],
        ["Total Orders", str(len(orders))],
        ["Delayed Orders", str(len(delayed_orders))],
        ["Critical Stock Products", str(len(critical_products))],
        ["Total Products", str(len(products))],
    ]
    summary_table = Table(summary_data, colWidths=[10*cm, 6*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#020617")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.8*cm))

    # Geciken siparişler
    story.append(Paragraph("Delayed Orders", styles["Heading2"]))
    if delayed_orders:
        order_data = [["Order ID", "Customer", "Status"]]
        for o in delayed_orders:
            order_data.append([f"#{o.id}", o.customer, o.status])
        order_table = Table(order_data, colWidths=[4*cm, 8*cm, 4*cm])
        order_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ef4444")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fef2f2"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fecaca")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(order_table)
    else:
        story.append(Paragraph("No delayed orders. ✓", styles["Normal"]))
    story.append(Spacer(1, 0.8*cm))

    # Kritik stoklar
    story.append(Paragraph("Critical Stock Products", styles["Heading2"]))
    if critical_products:
        product_data = [["Product", "Current Stock", "Critical Threshold"]]
        for p in critical_products:
            product_data.append([p.name, str(p.stock), str(p.critical_stock)])
        product_table = Table(product_data, colWidths=[8*cm, 4*cm, 4*cm])
        product_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f59e0b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fffbeb"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fde68a")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(product_table)
    else:
        story.append(Paragraph("All products are at healthy stock levels. ✓", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    filename = f"koopilot_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )