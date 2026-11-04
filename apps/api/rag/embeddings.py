
import requests
from typing import List

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "all-minilm"
EMBEDDING_DIMENSION = 384


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for document chunks using Ollama.
    """

    if not texts:
        return []

    all_embeddings = []
    batch_size = 8

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "input": batch,
                    "truncate": True
                },
                timeout=180
            )

            response.raise_for_status()

            data = response.json()
            embeddings = data.get("embeddings", [])

            if len(embeddings) != len(batch):
                raise ValueError("Embedding count mismatch.")

            for embedding in embeddings:
                if len(embedding) != EMBEDDING_DIMENSION:
                    raise ValueError(
                        f"Expected {EMBEDDING_DIMENSION} dimensions, "
                        f"received {len(embedding)}."
                    )

            all_embeddings.extend(embeddings)

        except requests.RequestException as error:
            raise RuntimeError(
                f"Ollama embedding request failed: {error}"
            ) from error

    return all_embeddings


def generate_query_embedding(query: str) -> List[float]:
    """
    Generate an embedding for a user's search query.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    embeddings = generate_embeddings([query])

    return embeddings[0]
