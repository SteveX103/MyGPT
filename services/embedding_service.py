import ollama


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


def generate_embeddings(
    chunks: list[str]
) -> list[list[float]]:

    if not chunks:
        return []

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=chunks
    )

    return response["embeddings"]