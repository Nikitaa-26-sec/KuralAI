
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag.retrieval import retrieve_relevant_chunks
from rag.llm import generate_answer

app = FastAPI(
    title="KuralAI Legal Assistance API",
    description="RAG-powered Indian legal information assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = "English"


class Source(BaseModel):
    title: str
    page: int
    chunk: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []


@app.get("/")
def root():
    return {"message": "KuralAI API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    # Step 1: Retrieve relevant legal passages
    retrieved_chunks = retrieve_relevant_chunks(
        query=req.message,
        top_k=4
    )

    # Step 2: Generate an answer using retrieved context
    answer = generate_answer(
        question=req.message,
        retrieved_chunks=retrieved_chunks,
        language=req.language
    )

    # Step 3: Prepare source references
    sources = [
        Source(
            title=chunk["source"],
            page=chunk["page"],
            chunk=chunk["chunk"]
        )
        for chunk in retrieved_chunks
    ]

    return ChatResponse(
        answer=answer,
        sources=sources
    )
