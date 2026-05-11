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
    Product(name="Olive Oil", stock=120, critical_stock=30),
    Product(name="Honey", stock=15, critical_stock=25),
    Product(name="Tomatoes", stock=40, critical_stock=50),
    Product(name="Cheese", stock=18, critical_stock=20),
    Product(name="Milk", stock=75, critical_stock=25),
    Product(name="Pasta", stock=200, critical_stock=50),
    Product(name="Coffee", stock=22, critical_stock=30),
    Product(name="Tea", stock=90, critical_stock=40),
    Product(name="Eggs", stock=35, critical_stock=30),
    Product(name="Butter", stock=12, critical_stock=20),
    Product(name="Jam", stock=28, critical_stock=35),
    Product(name="Flour", stock=160, critical_stock=60),
    Product(name="Lentils", stock=55, critical_stock=45),
    Product(name="Chickpeas", stock=42, critical_stock=40),
    Product(name="Rice", stock=95, critical_stock=50),
    Product(name="Tomato Paste", stock=19, critical_stock=25),
    Product(name="Apples", stock=85, critical_stock=40),
    Product(name="Oranges", stock=33, critical_stock=45),
    Product(name="Yogurt", stock=26, critical_stock=30),
    Product(name="Walnuts", stock=14, critical_stock=20),
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
    Order(customer="Emily Johnson", product="Olive Oil", quantity=2, status="Shipped", cargo_id=5001),
    Order(customer="Michael Brown", product="Honey", quantity=1, status="Delayed", cargo_id=5002),
    Order(customer="Sophia Wilson", product="Cheese", quantity=4, status="Delivered", cargo_id=5003),
    Order(customer="Daniel Miller", product="Milk", quantity=6, status="Preparing", cargo_id=5004),
    Order(customer="Olivia Davis", product="Coffee", quantity=3, status="Delayed", cargo_id=5005),
    Order(customer="James Taylor", product="Pasta", quantity=10, status="Shipped", cargo_id=5006),
    Order(customer="Benjamin Moore", product="Butter", quantity=2, status="Preparing", cargo_id=5004),
    Order(customer="Charlotte Anderson", product="Tea", quantity=5, status="Delivered", cargo_id=5007),
    Order(customer="William Thomas", product="Tomatoes", quantity=8, status="Delayed", cargo_id=5005),
    Order(customer="Amelia Jackson", product="Eggs", quantity=12, status="Shipped", cargo_id=5006),
    Order(customer="Lucas White", product="Jam", quantity=2, status="Preparing", cargo_id=5008),
    Order(customer="Harper Harris", product="Flour", quantity=15, status="Shipped", cargo_id=5010),
    Order(customer="Henry Martin", product="Lentils", quantity=7, status="Delivered", cargo_id=5011),
    Order(customer="Evelyn Thompson", product="Chickpeas", quantity=5, status="Preparing", cargo_id=5012),
    Order(customer="Alexander Garcia", product="Rice", quantity=9, status="Shipped", cargo_id=5014),
    Order(customer="Abigail Martinez", product="Tomato Paste", quantity=4, status="Delayed", cargo_id=5009),
    Order(customer="Matthew Robinson", product="Apples", quantity=11, status="Delivered", cargo_id=5015),
    Order(customer="Ella Clark", product="Oranges", quantity=6, status="Delayed", cargo_id=5013),
    Order(customer="David Rodriguez", product="Yogurt", quantity=3, status="Preparing", cargo_id=5008),
    Order(customer="Scarlett Lewis", product="Walnuts", quantity=2, status="Delayed", cargo_id=5013),
    Order(customer="Joseph Lee", product="Honey", quantity=2, status="Shipped", cargo_id=5010),
    Order(customer="Grace Walker", product="Tomatoes", quantity=10, status="Preparing", cargo_id=5012),
    Order(customer="Samuel Hall", product="Coffee", quantity=4, status="Delayed", cargo_id=5009),
    Order(customer="Victoria Allen", product="Butter", quantity=1, status="Delivered", cargo_id=5011),
    Order(customer="Christopher Young", product="Tomato Paste", quantity=6, status="Shipped", cargo_id=5014),
]

    db.add_all(products)
    db.add_all(shipments)
    db.add_all(orders)

    db.commit()
    db.close()