
from app.agents.support_graph import support_graph

if __name__ == "__main__":

    result = support_graph.invoke({
        "ticket_id": "TKT00001"
    })

    print("\n========== TICKET INVESTIGATION ==========")
    print(result.get("ticket"))

    print("\n========== BOOKING DETAILS ==========")
    print(result.get("booking"))

    print("\n========== CUSTOMER DETAILS ==========")
    print(result.get("customer"))

    print("\n========== CUSTOMER HISTORY ==========")
    print(result.get("customer_history"))

    print("\n========== DATA INTEGRITY WARNINGS ==========")
    print(result.get("data_integrity_warnings"))

    print("\n========== RETRIEVED KNOWLEDGE ==========")

    for article in result.get("knowledge", []):
        print(article["id"], article["text"])

    print("\n========== GEMINI REASONING ==========")

    analysis = result.get("analysis")

    if analysis:
        for key, value in analysis.items():
            print(f"\n{key}: {value}")

    if result.get("error"):
        print("\nERROR:", result["error"])
