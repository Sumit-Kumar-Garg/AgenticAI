
from app.rag.retriever import retrieve_knowledge


if __name__ == "__main__":
    query = (
        "The customer has a confirmed hotel booking, "
        "but the hotel cannot find the reservation."
    )

    results = retrieve_knowledge(query, top_k=3)

    print("\nSearch query:", query)
    print("\nRetrieved knowledge:")

    for result in results:
        print("\n------------------------------")
        print("Article ID:", result["id"])
        print("Issue:", result["metadata"]["issue"])
        print("Content:", result["text"])
        print("Distance:", result["distance"])
