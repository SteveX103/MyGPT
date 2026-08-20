from services.document_parser_service import extract_text
from services.document_chunking_service import chunk_text


file_path = r"E:\Project\Personal\MyGPT\uploads\6a633fa030a0e0f783681299\CCAT & CCEE Deployment Manual final.pdf"


text = extract_text(file_path)

print("Total characters:", len(text))

chunks = chunk_text(text)

print("Total chunks:", len(chunks))

print("\n--- FIRST CHUNK ---\n")
print(chunks[0])

print("\n--- SECOND CHUNK ---\n")
print(chunks[1])