
import os
import json

from dotenv import load_dotenv
from google import genai
from app.llm import get_api_key
from app.llm import get_model
from google.genai import types

load_dotenv(override=True)

api_key = get_api_key() 

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in .env")

client = genai.Client(api_key=api_key)

MODEL_NAME = get_model()  # e.g., "gemini-2.5-flash"


def analyze_support_case(case_context: dict) -> dict:

    system_instruction = """
    You are an expert hotel booking support analyst.

    Analyze the ticket using only the supplied information.

    Rules:
    1. Never invent customer, booking or payment information.
    2. Use retrieved knowledge articles as supporting evidence.
    3. Treat data integrity warnings as serious issues.
    4. If the ticket customer and booking customer do not match,
       do not recommend customer-specific financial action.
    5. Clearly distinguish confirmed facts from likely causes.
    6. Escalate to a human when evidence is insufficient or
       data integrity problems exist.
    7. Do not claim that any action has already been completed.
    """

    prompt = f"""
    Analyze this hotel support case.

    CASE DATA:
    {json.dumps(case_context, indent=2)}

    Return a structured support recommendation.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "category": {
                        "type": "STRING",
                        "enum": [
                            "BOOKING_CONFIRMATION",
                            "PAYMENT",
                            "CANCELLATION",
                            "REFUND",
                            "TECHNICAL",
                            "OTHER"
                        ]
                    },
                    "likely_root_cause": {
                        "type": "STRING"
                    },
                    "supporting_articles": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "recommended_action": {
                        "type": "STRING"
                    },
                    "confidence": {
                        "type": "NUMBER"
                    },
                    "requires_human": {
                        "type": "BOOLEAN"
                    },
                    "reasoning": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "category",
                    "likely_root_cause",
                    "supporting_articles",
                    "recommended_action",
                    "confidence",
                    "requires_human",
                    "reasoning"
                ]
            }
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    result = json.loads(response.text)

    if not 0 <= result["confidence"] <= 1:
        raise ValueError("Confidence must be between 0 and 1")

    return result
