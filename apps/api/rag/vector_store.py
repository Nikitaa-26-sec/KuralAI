import os
from pathlib import Path

import chromadb

# This file is apps/api/rag/vector_store.py; parents[3] is the repository root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = Path(os.getenv("KURALAI_CHROMA_PATH", str(
    PROJECT_ROOT / "data" / "processed" / "chroma_db"
)))
DB_PATH.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_or_create_collection(
    name="kuralai_legal_knowledge",
    metadata={"hnsw:space": "cosine"},
)


def store_chunks(chunks: list[dict], embeddings: list[list[float]]) -> int:
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have equal lengths.")
    if not chunks:
        return 0

    ids, documents, metadatas = [], [], []
    for item in chunks:
        source = str(item["source"])
        page = int(item["page"])
        chunk_number = int(item["chunk"])
        # Stable IDs make re-indexing the same source update rather than duplicate it.
        safe_source = source.replace("/", "_").replace("\\\\", "_")
        ids.append(f"{safe_source}_page_{page}_chunk_{chunk_number}")
        documents.append(str(item["text"]))
        metadatas.append({
            "source": source,
            "page": page,
            "chunk": chunk_number,
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(ids)


def clear_collection() -> int:
    existing = collection.get()
    ids = existing.get("ids", [])
    if ids:
        collection.delete(ids=ids)
    return len(ids)
