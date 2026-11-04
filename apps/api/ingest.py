from pathlib import Path

from rag.ingestion import extract_pdf_pages
from rag.chunking import create_document_chunks
from rag.embeddings import generate_embeddings
from rag.vector_store import store_chunks

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_FOLDER = PROJECT_ROOT / "data" / "raw" / "legal_documents"


def index_pdf(pdf_path: Path) -> int:
    print(f"\nProcessing: {pdf_path.name}")
    pages = extract_pdf_pages(pdf_path)
    if not pages:
        print("No extractable text found. If this is a scanned PDF, OCR is required.")
        return 0

    chunks = create_document_chunks(pages)
    if not chunks:
        return 0

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = generate_embeddings([item["text"] for item in chunks])
    indexed = store_chunks(chunks, embeddings)
    print(f"Indexed {indexed} chunks from {pdf_path.name}.")
    return indexed


def index_documents() -> int:
    DOCUMENT_FOLDER.mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(DOCUMENT_FOLDER.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF documents found. Add official legal PDFs to: {DOCUMENT_FOLDER}")
        return 0

    total = 0
    for pdf_path in pdf_files:
        try:
            total += index_pdf(pdf_path)
        except Exception as exc:
            print(f"Failed to index {pdf_path.name}: {exc}")

    print(f"\nDocument indexing completed. Total chunks indexed: {total}")
    return total


if __name__ == "__main__":
    index_documents()
