
from app.agents.support_graph import support_graph

if __name__ == "__main__":

    ticket_id = "TKT00001"

    result = support_graph.invoke({
        "ticket_id": ticket_id
    })

    print("\n========== TICKET INVESTIGATION ==========")
    print(result.get("ticket"))

    print("\n========== BOOKING DETAILS ==========")
    print(result.get("booking"))

    print("\n========== CUSTOMER DETAILS ==========")
    print(result.get("customer"))

    print("\n========== CUSTOMER HISTORY ==========")
    print(result.get("customer_history"))

    print("\n========== RETRIEVED KNOWLEDGE ==========")

    

    for article in result.get("knowledge", []):
        print("\nArticle:", article["id"])
        print("Content:", article["text"])
        print("Distance:", article["distance"])

    print("\n========== DATA INTEGRITY WARNINGS ==========")
    for warning in result.get("data_integrity_warnings", []):
        print(warning)

    if not result.get("data_integrity_warnings"):
        print("No data integrity issues found.")

    if result.get("error"):
        print("\nERROR:", result["error"])
