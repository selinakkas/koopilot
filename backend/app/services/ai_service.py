import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_ai_response(user_message: str, context: dict) -> str:
    prompt = f"""
You are Koopilot, an AI-powered operations assistant for small businesses.

Use ONLY the operational data below to answer the user's question.
If the answer is not available in the data, say that you cannot find it.

Operational Data:
Orders:
{context["orders"]}

Products:
{context["products"]}

Cargos:
{context["cargos"]}

User question:
{user_message}

Provide professional, concise operational insights in clear English.
Include useful context when possible.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI operations assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content


def analyze_complaint_with_ai(customer_message: str) -> dict:
    prompt = f"""
You are Koopilot, an AI operations assistant for small businesses.

Analyze the following customer complaint and return:
1. severity: LOW, MEDIUM, or HIGH
2. category: one of Shipment, Stock, Product Quality, General
3. ai_response: a friendly, empathetic response to send to the customer
4. recommended_action: a clear operational action for the internal team

Customer complaint:
{customer_message}

Return ONLY valid JSON with these exact keys:
severity, category, ai_response, recommended_action
No markdown, no code blocks, just raw JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional operations support analyst. Always respond with raw JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    return json.loads(content)