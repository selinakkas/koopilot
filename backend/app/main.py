from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.dashboard import router as dashboard_router
from app.routes.orders import router as orders_router
from app.routes.products import router as products_router

app = FastAPI(title="Koopilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router)
app.include_router(products_router)
app.include_router(dashboard_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Koopilot backend is running"}