
from pypdf import PdfReader


def extract_pdf_pages(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    return pages

