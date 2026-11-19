"""Tool-calling investigator agent.

The model gathers evidence with allow-listed, read-only tools (ticket, booking,
customer, history, knowledge-base search) and then explains the likely cause and
the next action. Works with any OpenAI-compatible provider (Gemini, Groq, OpenAI);
see app/llm.py.
"""
import json

from app.agents.tool_definitions import TOOLS
from app.agents.tool_executor import execute_tool
from app.llm import get_chat_client

MAX_ITERATIONS = 8


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


def _run_tool(tool_call):
    """Execute one tool call. Errors go back to the model instead of crashing the loop."""
    name = tool_call.function.name
    arguments = {}
    try:
        arguments = json.loads(tool_call.function.arguments or "{}")
        result = execute_tool(name, arguments)
    except Exception as exc:
        result = {"error": f"{type(exc).__name__}: {exc}"}
    if result is None:
        result = {"error": "not found"}
    return name, arguments, result


def investigate_ticket(ticket_id: str):
    client, model = get_chat_client()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Investigate support ticket {ticket_id}. "
                "Find the cause of the issue and recommend "
                "the next action."
            ),
        },
    ]

    execution_log = []

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # No more tool calls: the agent has finished
        if not assistant_message.tool_calls:
            return {
                "ticket_id": ticket_id,
                "investigation": assistant_message.content,
                "tool_execution_log": execution_log,
            }

        # Keep the assistant's tool-call turn in the conversation
        messages.append(assistant_message.model_dump(exclude_none=True))

        for tool_call in assistant_message.tool_calls:
            name, arguments, result = _run_tool(tool_call)

            execution_log.append({"tool": name, "arguments": arguments, "result": result})

            # Send the tool result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

    raise RuntimeError(f"Agent exceeded {MAX_ITERATIONS} tool iterations")
