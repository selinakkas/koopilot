from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


class ComplaintRequest(BaseModel):
    customer_message: str


@router.post("/analyze")
def analyze_complaint(request: ComplaintRequest):
    message = request.customer_message.lower()

    severity = "LOW"
    recommended_action = "Monitor the complaint and respond with a standard support message."

    if "late" in message or "delayed" in message or "not arrived" in message:
        severity = "HIGH"
        recommended_action = (
            "Prioritize shipment follow-up, inform the customer proactively, "
            "and check if the related order has a delayed cargo status."
        )

    elif "stock" in message or "available" in message:
        severity = "MEDIUM"
        recommended_action = (
            "Check product availability and provide the customer with an updated stock status."
        )

    elif "wrong" in message or "damaged" in message:
        severity = "HIGH"
        recommended_action = (
            "Escalate to support team, verify the order details, and offer replacement or refund options."
        )

    return {
        "severity": severity,
        "summary": request.customer_message,
        "recommended_action": recommended_action
    }