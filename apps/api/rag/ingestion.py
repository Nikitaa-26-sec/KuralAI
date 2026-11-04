from pathlib import Path
from pypdf import PdfReader


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """Extract non-empty text from each page of a PDF."""
    path = Path(pdf_path)
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise ValueError("A valid PDF file path is required.")

    reader = PdfReader(str(path))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError(f"Encrypted PDF cannot be read: {path.name}") from exc

    pages: list[dict] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": page_number, "text": text, "source": path.name})
    return pages
