
TOOLS = [

   
{
    "type": "function",
    "function": {
        "name": "search_support_knowledge",
        "description": (
            "Search the hotel support knowledge base for "
            "relevant troubleshooting guides, issue explanations "
            "and recommended resolutions. Use this when investigating "
            "the cause of a ticket or deciding the next action."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A natural-language description of the "
                        "customer's issue or the knowledge needed."
                    )
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of relevant articles to retrieve."
                }
            },
            "required": ["query", "top_k"],
            "additionalProperties": False
        }
    }
},
 {
        "type": "function",
        "function": {
            "name": "lookup_ticket",
            "description": (
                "Retrieve support ticket details using "
                "the ticket ID. Use this first when "
                "investigating a support ticket."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Unique support ticket ID"
                    }
                },
                "required": ["ticket_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "lookup_booking",
            "description": (
                "Retrieve booking details, booking status "
                "and associated hotel information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string",
                        "description": "Unique booking ID"
                    }
                },
                "required": ["booking_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "lookup_customer",
            "description": (
                "Retrieve customer profile using customer ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique customer ID"
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "lookup_customer_history",
            "description": (
                "Retrieve historical support tickets "
                "for a customer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique customer ID"
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    }
]
