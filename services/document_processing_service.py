from pathlib import Path

from database.mongodb import documents_collection

from services.document_parser_service import extract_text
from services.document_chunking_service import chunk_text
from services.embedding_service import generate_embeddings
from services.chroma_service import add_chunks

from bson import ObjectId

def process_document(
    document_id: str,
    user_id: str,
    knowledge_base_id: str,
    file_path: str,
    filename: str
):
    try:

        # ------------------------------------------------
        # 1. Update status → processing
        # ------------------------------------------------

        documents_collection.update_one(
            {
                 "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "status": "processing"
                }
            }
        )

        # ------------------------------------------------
        # 2. Verify physical file
        # ------------------------------------------------

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # ------------------------------------------------
        # 3. Extract text
        # ------------------------------------------------

        text = extract_text(
            str(path)
        )

        if not text.strip():
            raise ValueError(
                "No text could be extracted from document"
            )

        # ------------------------------------------------
        # 4. Chunk text
        # ------------------------------------------------

        chunks = chunk_text(text)

        if not chunks:
            raise ValueError(
                "No chunks generated from document"
            )

        # ------------------------------------------------
        # 5. Generate embeddings
        # ------------------------------------------------

        embeddings = generate_embeddings(
            chunks
        )

        # ------------------------------------------------
        # 6. Store in ChromaDB
        # ------------------------------------------------

        chunk_count = add_chunks(
            knowledge_base_id=knowledge_base_id,
            document_id=document_id,
            user_id=user_id,
            filename=filename,
            chunks=chunks,
            embeddings=embeddings
        )

        # ------------------------------------------------
        # 7. Mark document as processed
        # ------------------------------------------------

        documents_collection.update_one(
            {
                 "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "status": "processed",
                    "chunk_count": chunk_count
                }
            }
        )

    except Exception as e:

        documents_collection.update_one(
            {
                 "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "status": "failed",
                    "processing_error": str(e)
                }
            }
        )

        print(
            f"Document processing failed: {e}"
        )