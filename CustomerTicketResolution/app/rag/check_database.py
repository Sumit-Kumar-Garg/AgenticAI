from app.rag.vector_store import collection

print("Collection name:", collection.name)

print("Total documents:", collection.count())

results = collection.get(
    limit=5,
    include=["documents", "metadatas"]
)

for i in range(len(results["ids"])):

    print("\nID:", results["ids"][i])
    print("Document:", results["documents"][i])
    print("Metadata:", results["metadatas"][i])