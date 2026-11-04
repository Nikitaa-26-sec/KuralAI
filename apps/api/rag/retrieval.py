
from rag.embeddings import generate_query_embedding
from rag.vector_store import collection

# Relaxed threshold for cosine distance.
MAX_DISTANCE = 0.85


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 4,
    max_distance: float = MAX_DISTANCE,
) -> list[dict]:

    if not query or not query.strip():
        return []

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not 0.0 <= max_distance <= 2.0:
        raise ValueError("max_distance must be between 0 and 2.")

    total = collection.count()

    if total == 0:
        return []

    query_embedding = generate_query_embedding(query.strip())

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total),
        include=["documents", "metadatas", "distances"],
    )

    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    matches = []

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        if not document or distance is None:
            continue

        distance = float(distance)

        if distance > max_distance:
            continue

        metadata = metadata or {}

        matches.append({
            "text": document,
            "source": metadata.get("source", "Unknown"),
            "page": int(metadata.get("page", 0)),
            "chunk": int(metadata.get("chunk", 0)),
            "distance": distance,
        })

    return matches
