import chromadb
from pathlib import Path


CHROMA_PATH = Path("data/chroma_db")
COLLECTION_NAME = "hotel_support_knowledge"


client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


def store_documents(chunks, embeddings):
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match")

    if not chunks:
        return 0

    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        embeddings=embeddings
    )

    return len(chunks)


def search_documents(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    if not results["ids"] or not results["ids"][0]:
        return matches

    for i in range(len(results["ids"][0])):
        matches.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matches
