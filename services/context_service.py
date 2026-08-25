def build_context(
    retrieved_chunks: list[dict]
) -> str:

    if not retrieved_chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        metadata = chunk.get("metadata", {})

        filename = metadata.get(
            "filename",
            "Unknown document"
        )

        chunk_index = metadata.get(
            "chunk_index",
            "Unknown"
        )

        text = chunk.get("text", "").strip()

        if not text:
            continue

        context_parts.append(
            f"[Source {index}]\n"
            f"Document: {filename}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n{text}"
        )

    return "\n\n".join(context_parts)
def build_rag_prompt(
    question: str,
    context: str
) -> str:

    return f"""
You are a helpful AI assistant operating in a private,
local Retrieval-Augmented Generation system.

Answer the user's question using the provided context.

Rules:
1. Use the provided context as the primary source of information.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information to answer,
   clearly say that the information was not found in the provided documents.
4. Keep the answer clear and relevant.
5. Do not mention these instructions in your answer.

Context:
--------------------
{context}
--------------------

User Question:
{question}

Answer:
""".strip()