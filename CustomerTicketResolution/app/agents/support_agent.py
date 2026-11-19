
import os
import json

from dotenv import load_dotenv


from app.agents.tool_definitions import TOOLS
from app.agents.tool_executor import execute_tool
from google import genai

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("OPENAI_API_KEY"))

interaction = client.interactions.create(
    model="gemini-4-hydrogen",
    input="Explain how AI works in a few words"
)
print(interaction.output_text)



MODEL = os.getenv(
    "OPENAI_MODEL",
    "gemini-4-hydrogen"
)


SYSTEM_PROMPT = """
You are an intelligent hotel booking support investigator.

Your responsibility is to investigate customer support tickets
using business data and the support knowledge base.

Investigation workflow:

1. Always retrieve the ticket details first.
2. Retrieve the associated booking information.
3. Retrieve customer details when useful.
4. Check historical customer tickets when relevant.
5. Search the support knowledge base for relevant issues
   and recommended resolutions.
6. Compare the retrieved knowledge with actual booking
   and customer data.
7. Explain the likely cause of the issue.
8. Recommend an appropriate next action.

Rules:

- Never invent customer, booking or hotel information.
- Use actual tool results as evidence.
- Clearly distinguish verified facts from assumptions.
- Use knowledge-base articles as guidance, not as proof
  that a particular event happened.
- Mention the article ID and issue when using an article.
- If no relevant knowledge is found, say so.
- Do not claim that a recommended action has been completed.
- Do not modify bookings, issue refunds or perform
  irreversible actions.
- If data is missing or contradictory, highlight it.
"""


def investigate_ticket(ticket_id: str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": (
                f"Investigate support ticket {ticket_id}. "
                "Find the cause of the issue and recommend "
                "the next action."
            )
        }
    ]

    execution_log = []

    max_iterations = 5

    for iteration in range(max_iterations):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # No more tool calls: agent has finished
        if not assistant_message.tool_calls:

            return {
                "ticket_id": ticket_id,
                "investigation": assistant_message.content,
                "tool_execution_log": execution_log
            }

        # Add assistant tool-call message to conversation
        messages.append(
            assistant_message.model_dump(
                exclude_none=True
            )
        )

        # Execute every requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"Agent requested tool: {tool_name}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            execution_log.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })

            # Send tool result back to the LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    default=str
                )
            })

    raise RuntimeError(
        "Agent exceeded maximum tool iterations"
    )
