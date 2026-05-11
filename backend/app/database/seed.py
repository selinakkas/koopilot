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
        Product(name="Zeytinyağı", stock=120, critical_stock=30),
        Product(name="Bal", stock=15, critical_stock=25),
        Product(name="Domates", stock=40, critical_stock=50),
        Product(name="Peynir", stock=18, critical_stock=20),
        Product(name="Süt", stock=75, critical_stock=25),
        Product(name="Makarna", stock=200, critical_stock=50),
        Product(name="Kahve", stock=22, critical_stock=30),
        Product(name="Çay", stock=90, critical_stock=40),
        Product(name="Yumurta", stock=35, critical_stock=30),
        Product(name="Tereyağı", stock=12, critical_stock=20),
        Product(name="Reçel", stock=28, critical_stock=35),
        Product(name="Un", stock=160, critical_stock=60),
        Product(name="Mercimek", stock=55, critical_stock=45),
        Product(name="Nohut", stock=42, critical_stock=40),
        Product(name="Pirinç", stock=95, critical_stock=50),
        Product(name="Salça", stock=19, critical_stock=25),
        Product(name="Elma", stock=85, critical_stock=40),
        Product(name="Portakal", stock=33, critical_stock=45),
        Product(name="Yoğurt", stock=26, critical_stock=30),
        Product(name="Ceviz", stock=14, critical_stock=20),
    ]

    shipments = [
        Shipment(cargo_id=5001, status="On the way", estimated_delivery="Tomorrow"),
        Shipment(cargo_id=5002, status="Delayed", estimated_delivery="2 days later"),
        Shipment(cargo_id=5003, status="Delivered", estimated_delivery="Delivered"),
        Shipment(cargo_id=5004, status="Preparing", estimated_delivery="3 days"),
        Shipment(cargo_id=5005, status="Delayed", estimated_delivery="5 days later"),
        Shipment(cargo_id=5006, status="On the way", estimated_delivery="Tonight"),
        Shipment(cargo_id=5007, status="Delivered", estimated_delivery="Delivered"),
        Shipment(cargo_id=5008, status="Preparing", estimated_delivery="Tomorrow"),
        Shipment(cargo_id=5009, status="Delayed", estimated_delivery="4 days later"),
        Shipment(cargo_id=5010, status="On the way", estimated_delivery="2 days"),
        Shipment(cargo_id=5011, status="Delivered", estimated_delivery="Delivered"),
        Shipment(cargo_id=5012, status="Preparing", estimated_delivery="3 days"),
        Shipment(cargo_id=5013, status="Delayed", estimated_delivery="6 days later"),
        Shipment(cargo_id=5014, status="On the way", estimated_delivery="Tomorrow"),
        Shipment(cargo_id=5015, status="Delivered", estimated_delivery="Delivered"),
    ]

    orders = [
        Order(customer="Ayşe Demir", product="Zeytinyağı", quantity=2, status="Shipped", cargo_id=5001),
        Order(customer="Mehmet Kaya", product="Bal", quantity=1, status="Delayed", cargo_id=5002),
        Order(customer="Zeynep Aydın", product="Peynir", quantity=4, status="Delivered", cargo_id=5003),
        Order(customer="Ahmet Yılmaz", product="Süt", quantity=6, status="Preparing", cargo_id=5004),
        Order(customer="Elif Çetin", product="Kahve", quantity=3, status="Delayed", cargo_id=5005),
        Order(customer="Burak Şahin", product="Makarna", quantity=10, status="Shipped", cargo_id=5006),
        Order(customer="Can Özkan", product="Tereyağı", quantity=2, status="Preparing", cargo_id=5004),
        Order(customer="Melisa Kurt", product="Çay", quantity=5, status="Delivered", cargo_id=5007),
        Order(customer="Kerem Arslan", product="Domates", quantity=8, status="Delayed", cargo_id=5005),
        Order(customer="Seda Yıldız", product="Yumurta", quantity=12, status="Shipped", cargo_id=5006),
        Order(customer="Mert Koç", product="Reçel", quantity=2, status="Preparing", cargo_id=5008),
        Order(customer="Derya Sönmez", product="Un", quantity=15, status="Shipped", cargo_id=5010),
        Order(customer="Emre Polat", product="Mercimek", quantity=7, status="Delivered", cargo_id=5011),
        Order(customer="Nazlı Kara", product="Nohut", quantity=5, status="Preparing", cargo_id=5012),
        Order(customer="Ali Ergin", product="Pirinç", quantity=9, status="Shipped", cargo_id=5014),
        Order(customer="Gizem Aksoy", product="Salça", quantity=4, status="Delayed", cargo_id=5009),
        Order(customer="Okan Yavuz", product="Elma", quantity=11, status="Delivered", cargo_id=5015),
        Order(customer="Ece Uslu", product="Portakal", quantity=6, status="Delayed", cargo_id=5013),
        Order(customer="Tolga Baş", product="Yoğurt", quantity=3, status="Preparing", cargo_id=5008),
        Order(customer="İrem Deniz", product="Ceviz", quantity=2, status="Delayed", cargo_id=5013),
        Order(customer="Hakan Güner", product="Bal", quantity=2, status="Shipped", cargo_id=5010),
        Order(customer="Selma Çelik", product="Domates", quantity=10, status="Preparing", cargo_id=5012),
        Order(customer="Onur Aksu", product="Kahve", quantity=4, status="Delayed", cargo_id=5009),
        Order(customer="Bahar Eren", product="Tereyağı", quantity=1, status="Delivered", cargo_id=5011),
        Order(customer="Deniz Topal", product="Salça", quantity=6, status="Shipped", cargo_id=5014),
    ]

    db.add_all(products)
    db.add_all(shipments)
    db.add_all(orders)

    db.commit()
    db.close()