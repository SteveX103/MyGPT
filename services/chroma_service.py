import chromadb


CHROMA_PATH = "./chroma_db"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def get_collection(knowledge_base_id: str):

    collection_name = f"kb_{knowledge_base_id}"

    return client.get_or_create_collection(
        name=collection_name
    )

# this is for adding chunks to the collection.
def add_chunks(
    knowledge_base_id: str,
    document_id: str,
    user_id: str,
    filename: str,
    chunks: list[str],
    embeddings: list[list[float]]
):

    collection = get_collection(
        knowledge_base_id
    )

    ids = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"{document_id}_chunk_{index}"
        )

        ids.append(chunk_id)

        metadatas.append({
            "user_id": user_id,
            "knowledge_base_id": knowledge_base_id,
            "document_id": document_id,
            "filename": filename,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)

#this is  search function
def search_chunks(
    knowledge_base_id: str,
    query_embedding: list[float],
    top_k: int = 5
):

    collection = get_collection(
        knowledge_base_id
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results