import os

from openai import OpenAI
from dotenv import load_dotenv

from app.models.ticket import TicketAnalysis

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


def analyze_ticket(description: str) -> TicketAnalysis:

    instructions = """
    You are an intelligent customer support ticket
    classification system.

    Analyze the customer support ticket.

    Identify:
    1. Ticket category
    2. Priority
    3. Confidence score between 0 and 1
    4. Recommended next action
    5. Whether human intervention is required

    Rules:
    - Do not invent booking or payment information.
    - Payment disputes and potential financial loss
      should receive appropriate priority.
    - Security issues should be escalated.
    - If information is insufficient, request human review.
    - Be conservative when assigning confidence.
    """

    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": description
            }
        ],
        response_format=TicketAnalysis
    )

    result = response.choices[0].message.parsed

    if result is None:
        raise ValueError("AI did not return a valid analysis")

    return result