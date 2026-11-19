from app.agents.support_tools import search_support_knowledge

from app.agents.support_tools import (
    lookup_ticket,
    lookup_booking,
    lookup_customer,
    lookup_customer_history
)


TOOL_REGISTRY = {
    "lookup_ticket": lookup_ticket,
    "lookup_booking": lookup_booking,
    "lookup_customer": lookup_customer,
    "lookup_customer_history": lookup_customer_history,
    "search_support_knowledge": search_support_knowledge
}


def execute_tool(tool_name: str, arguments: dict):

    tool_function = TOOL_REGISTRY.get(tool_name)

    if tool_function is None:
        raise ValueError(
            f"Tool not allowed: {tool_name}"
        )

    return tool_function(**arguments)
