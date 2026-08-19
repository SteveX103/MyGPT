from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    path = Path(file_path)

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(
    file_path: str,
    content_type: str | None = None
) -> str:

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )