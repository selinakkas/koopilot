import os
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
2. summary: a short summary of the complaint
3. recommended_action: a clear operational action for the team

Customer complaint:
{customer_message}

Return your answer strictly as JSON with these keys:
severity, summary, recommended_action
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional operations support analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    import json
    return json.loads(content)