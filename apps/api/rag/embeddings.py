import os
from typing import List

import requests

OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://localhost:11434/api/embed")
EMBEDDING_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "all-minilm")
REQUEST_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "180"))


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using the configured local Ollama embedding model."""
    if not texts:
        return []

    all_embeddings: List[List[float]] = []
    batch_size = 16

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        try:
            response = requests.post(
                OLLAMA_EMBED_URL,
                json={"model": EMBEDDING_MODEL, "input": batch},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
            embeddings = payload.get("embeddings")

            if not isinstance(embeddings, list) or len(embeddings) != len(batch):
                raise RuntimeError(
                    "Ollama returned an unexpected embedding response. "
                    f"Check that model '{EMBEDDING_MODEL}' is installed."
                )

            for vector in embeddings:
                if not isinstance(vector, list) or not vector:
                    raise RuntimeError("Ollama returned an empty or invalid embedding.")
            all_embeddings.extend(embeddings)

        except requests.RequestException as exc:
            raise RuntimeError(
                "Could not reach Ollama's embedding endpoint. Start Ollama and "
                f"pull the '{EMBEDDING_MODEL}' model. Details: {exc}"
            ) from exc

    return all_embeddings


def generate_query_embedding(query: str) -> List[float]:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")
    vectors = generate_embeddings([query.strip()])
    if not vectors:
        raise RuntimeError("No query embedding was generated.")
    return vectors[0]
