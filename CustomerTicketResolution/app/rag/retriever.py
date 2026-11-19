from app.rag.embedding_service import generate_embeddings
from app.rag.vector_store import search_documents


def retrieve_knowledge(query: str, top_k: int = 3):
    query_embeddings = generate_embeddings([query])

    return search_documents(
        query_embedding=query_embeddings[0],
        top_k=top_k
    )
