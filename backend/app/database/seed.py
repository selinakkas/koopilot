from app.database.database import SessionLocal
from app.database.models import Product
from app.database.models import Shipment
from app.database.models import Order


def seed_database():
    db = SessionLocal()

    existing_orders = db.query(Order).first()

    if existing_orders:
        db.close()
        return

    products = [
        Product(
            name="Zeytinyağı",
            stock=120,
            critical_stock=30
        ),
        Product(
            name="Bal",
            stock=15,
            critical_stock=25
        ),
        Product(
            name="Domates",
            stock=40,
            critical_stock=50
        ),
    ]

    shipments = [
        Shipment(
            cargo_id=5001,
            status="On the way",
            estimated_delivery="Tomorrow"
        ),
        Shipment(
            cargo_id=5002,
            status="Delayed",
            estimated_delivery="2 days later"
        ),
    ]

    orders = [
        Order(
            customer="Ayşe Demir",
            product="Zeytinyağı",
            quantity=2,
            status="Shipped",
            cargo_id=5001
        ),
        Order(
            customer="Mehmet Kaya",
            product="Bal",
            quantity=1,
            status="Delayed",
            cargo_id=5002
        ),
    ]

    db.add_all(products)
    db.add_all(shipments)
    db.add_all(orders)

    db.commit()
    db.close()