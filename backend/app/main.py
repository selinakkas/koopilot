from fastapi import FastAPI

from app.routes.orders import router as orders_router

app = FastAPI(title="Koopilot API")

app.include_router(orders_router)


@app.get("/")
def root():
    return {"message": "Koopilot backend is running"}