from fastapi import HTTPException

from services.embedding_service import generate_embedding
from services.chroma_service import get_collection


def retrieve_relevant_chunks(
    user_id: str,
    knowledge_base_id: str,
    query: str,
    top_k: int = 5
):
    if not query or not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    # Convert question into an embedding
    query_embedding = generate_embedding(query)

    # Get the KB-specific collection
    collection = get_collection(
        knowledge_base_id
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved_chunks = []

    for index, document in enumerate(documents):

        metadata = metadatas[index]

        # Additional security validation
        if metadata.get("user_id") != user_id:
            continue

        if metadata.get("knowledge_base_id") != knowledge_base_id:
            continue

        retrieved_chunks.append({
            "text": document,
            "metadata": metadata,
            "distance": distances[index]
        })

    return retrieved_chunks