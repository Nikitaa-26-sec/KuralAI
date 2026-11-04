
from pathlib import Path

from rag.ingestion import extract_pdf_pages
from rag.chunking import create_document_chunks
from rag.embeddings import generate_embeddings
from rag.vector_store import store_chunks


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENT_FOLDER = (
    PROJECT_ROOT / "data" / "raw" / "legal_documents"
)


def index_documents():

    pdf_files = list(DOCUMENT_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found.")
        print(f"Place PDFs inside: {DOCUMENT_FOLDER}")
        return

    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        # Step 1: Extract PDF pages
        pages = extract_pdf_pages(str(pdf_path))

        if not pages:
            print("No pages extracted. Skipping document.")
            continue

        # Step 2: Attach source metadata to every page
        for page_data in pages:
            page_data["source"] = pdf_path.name

        # Step 3: Split extracted text into chunks
        chunks = create_document_chunks(pages)

        if not chunks:
            print("No extractable text found.")
            continue

        # Step 4: Extract chunk text
        texts = [chunk["text"] for chunk in chunks]

        print(f"Generating embeddings for {len(chunks)} chunks...")

        # Step 5: Generate embeddings
        embeddings = generate_embeddings(texts)

        # Step 6: Store chunks and embeddings
        store_chunks(chunks, embeddings)

        print(
            f"Successfully indexed {len(chunks)} chunks "
            f"from {pdf_path.name}."
        )

    print("\nDocument indexing completed!")


if __name__ == "__main__":
    index_documents()

