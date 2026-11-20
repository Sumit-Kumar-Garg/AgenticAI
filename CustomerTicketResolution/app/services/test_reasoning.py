
from app.services.reasoning_service import analyze_support_case

sample_case = {
    "ticket": {
        "ticket_id": "TKT00001",
        "description": "Refund not received",
        "priority": "LOW"
    },
    "booking": {
        "booking_id": "BOOK00853",
        "booking_status": "CONFIRMED",
        "amount": "305.56"
    },
    "data_integrity_warnings": [
        "Ticket customer ID CUST0449 does not match "
        "booking customer ID CUST0396"
    ],
    "knowledge": [
        {
            "id": "KB0004",
            "text": "Issue: Refund not received. "
                    "Solution: Check payment gateway transaction logs"
        }
    ],
    "customer_history": [
        {
            "description": "Payment failed",
            "status": "CLOSED"
        }
    ]
}

if __name__ == "__main__":

    result = analyze_support_case(sample_case)

    print("\n========== GEMINI ANALYSIS ==========")

    for key, value in result.items():
        print(f"\n{key}: {value}")
