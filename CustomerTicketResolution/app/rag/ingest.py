
from app.rag.document_loader import load_knowledge_articles
from app.rag.chunker import chunk_documents
from app.rag.embedding_service import generate_embeddings
from app.rag.vector_store import store_documents


def ingest_knowledge_base():
    print("Loading knowledge articles...")

    documents = load_knowledge_articles()
    print(f"Loaded {len(documents)} articles")

    print("Creating document chunks...")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    print("Storing vectors in ChromaDB...")

    count = store_documents(chunks, embeddings)

    print(f"Successfully indexed {count} documents")


if __name__ == "__main__":
    ingest_knowledge_base()
