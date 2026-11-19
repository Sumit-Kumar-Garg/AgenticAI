
def chunk_documents(documents):
    chunks = []

    for document in documents:
        chunks.append({
            "id": document["id"],
            "text": document["text"],
            "metadata": document["metadata"]
        })

    return chunks
