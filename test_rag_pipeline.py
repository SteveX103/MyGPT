from services.document_parser_service import extract_text
from services.document_chunking_service import chunk_text
from services.embedding_service import generate_embeddings


file_path = r"E:\Project\Personal\MyGPT\Documentation_Short.docx"


# 1. Extract
text = extract_text(file_path)

print("Characters:", len(text))


# 2. Chunk
chunks = chunk_text(text)

print("Chunks:", len(chunks))


# 3. Generate embeddings
embeddings = generate_embeddings(chunks)

print("Embeddings:", len(embeddings))

print(
    "Embedding dimensions:",
    len(embeddings[0])
)