from services.document_parser_service import extract_text


file_path = r"E:\Project\Personal\MyGPT\uploads\6a633fa030a0e0f783681299\CCAT & CCEE Deployment Manual final.pdf"

text = extract_text(file_path)

print("Characters extracted:", len(text))

print("\n--- TEXT PREVIEW ---\n")

print(text[:2000])