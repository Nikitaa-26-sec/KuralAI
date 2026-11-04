
from rag.embeddings import generate_query_embedding
from rag.vector_store import collection

# Initial threshold based on your observed retrieval results.
# Lower cosine distance means greater similarity.
MAX_DISTANCE = 0.55


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 4,
    max_distance: float = MAX_DISTANCE
):
    """
    Retrieve relevant legal passages and filter
    results using cosine distance.
    """

    if not query or not query.strip():
        return []

    total_documents = collection.count()

    if total_documents == 0:
        return []

    query_embedding = generate_query_embedding(query.strip())

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total_documents),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_chunks = []

    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]
    distances = results.get("distances") or [[]]

    if not documents[0]:
        return []

    for document, metadata, distance in zip(
        documents[0],
        metadatas[0],
        distances[0]
    ):

        if not document or not metadata:
            continue

        distance = float(distance)

        # Reject passages that are not sufficiently similar.
        if distance > max_distance:
            continue

        retrieved_chunks.append({
            "text": document,
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", 0),
            "chunk": metadata.get("chunk", 0),
            "distance": distance
        })

    return retrieved_chunks
