import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.database import get_db
from app.database.models import Product

router = APIRouter(prefix="/products", tags=["Products"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_products():
    with open(DATA_DIR / "products.json", "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return [
        {
            "id": product.id,
            "name": product.name,
            "stock": product.stock,
            "critical_stock": product.critical_stock,
        }
        for product in products
    ]


@router.get("/critical")
def get_critical_products():
    products = load_products()
    return [
        product for product in products
        if product["stock"] <= product["critical_stock"]
    ]


@router.get("/{product_id}")
def get_product(product_id: int):
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")