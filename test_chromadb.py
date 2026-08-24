from services.document_parser_service import extract_text
from services.document_chunking_service import chunk_text
from services.embedding_service import generate_embeddings
from services.chroma_service import add_chunks


USER_ID = "test-user"
KB_ID = "test-kb"
DOCUMENT_ID = "test-document"

FILE_PATH = r"E:\Project\Personal\MyGPT\uploads\6a633fa030a0e0f783681299\CCAT & CCEE Deployment Manual final.pdf"


# Extract
text = extract_text(FILE_PATH)

print("Characters:", len(text))


# Chunk
chunks = chunk_text(text)

print("Chunks:", len(chunks))


# Embed
embeddings = generate_embeddings(chunks)

print("Embeddings:", len(embeddings))


# Store
count = add_chunks(
    knowledge_base_id=KB_ID,
    document_id=DOCUMENT_ID,
    user_id=USER_ID,
    filename="test.pdf",
    chunks=chunks,
    embeddings=embeddings
)

print("Stored chunks:", count)