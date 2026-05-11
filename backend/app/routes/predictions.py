from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Product
from app.services.prediction_service import generate_predictions

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.get("/")
def get_predictions(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    return generate_predictions(products)