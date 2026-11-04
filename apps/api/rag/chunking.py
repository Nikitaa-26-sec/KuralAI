
def split_text(text: str, chunk_size=200, overlap=40):
    """
    Split legal document text into smaller overlapping chunks.
    """

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


def create_document_chunks(pages):
    """
    Create chunks while preserving document metadata.
    """

    all_chunks = []

    for page_data in pages:

        chunks = split_text(page_data["text"])

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "source": page_data["source"],
                "page": page_data["page"],
                "chunk": index
            })

    return all_chunks

