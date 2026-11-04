
from pathlib import Path
import chromadb

# Project root: C:\dev\kuralai
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "processed" / "chroma_db"

DB_PATH.mkdir(parents=True, exist_ok=True)

# Persistent vector database
client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_or_create_collection(
    name="kuralai_legal_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks(chunks, embeddings):
    """
    Store legal chunks, their embeddings and metadata.
    """

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have equal lengths.")

    if not chunks:
        return 0

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        source = chunk["source"]
        page = chunk["page"]
        chunk_number = chunk["chunk"]

        ids.append(
            f"{source}_page_{page}_chunk_{chunk_number}"
        )

        documents.append(chunk["text"])

        metadatas.append({
            "source": source,
            "page": page,
            "chunk": chunk_number
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)
def clear_collection():
    """
    Delete all indexed documents from the collection.
    """
    existing = collection.get()

    ids = existing["ids"]

    if ids:
        collection.delete(ids=ids)

    print(f"Deleted {len(ids)} indexed chunks.")