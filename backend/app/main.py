from fastapi import FastAPI

from app.routes.orders import router as orders_router
from app.routes.products import router as products_router

app = FastAPI(title="Koopilot API")

app.include_router(orders_router)
app.include_router(products_router)


@app.get("/")
def root():
    return {"message": "Koopilot backend is running"}