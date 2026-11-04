def split_text(text: str, chunk_size: int = 220, overlap: int = 40) -> list[str]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size.")

    words = text.split()
    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap

    return chunks


def create_document_chunks(pages: list[dict]) -> list[dict]:
    """Chunk pages while preserving source and page metadata."""
    all_chunks: list[dict] = []
    for page_data in pages:
        for index, chunk in enumerate(split_text(page_data["text"])):
            all_chunks.append({
                "text": chunk,
                "source": page_data.get("source", "Unknown"),
                "page": int(page_data["page"]),
                "chunk": index,
            })
    return all_chunks
