# KuralAI

**Her Voice. Her Rights. Her Kural.**

KuralAI is a multilingual Indian legal-information assistant built with Next.js, FastAPI, ChromaDB and a local Ollama language model. It uses retrieval-augmented generation (RAG): the backend retrieves passages from legal PDFs that you index, then asks the language model to answer using those passages.

> KuralAI is an educational legal-information tool, not a lawyer, emergency service, or substitute for professional legal advice. The quality and currency of answers depend on the legal documents you provide.

## Project structure

```text
KuralAI/
├── apps/
│   ├── api/
│   │   ├── main.py
│   │   ├── ingest.py
│   │   ├── requirements.txt
│   │   └── rag/
│   │       ├── ingestion.py
│   │       ├── chunking.py
│   │       ├── embeddings.py
│   │       ├── vector_store.py
│   │       ├── retrieval.py
│   │       └── llm.py
│   └── web/
│       └── app/
│           ├── page.tsx
│           └── chat/
│               ├── page.tsx
│               └── chat.module.css
├── data/
│   ├── raw/legal_documents/
│   └── processed/chroma_db/
└── .env.example
```

## Requirements

- Python 3.10 or newer
- Node.js 20.9 or newer
- Ollama installed and running
- The Ollama models `qwen2.5:1.5b` and `all-minilm`

## 1. Start Ollama

Open PowerShell:

```powershell
ollama pull qwen2.5:1.5b
ollama pull all-minilm
ollama list
```

Keep Ollama running. Its default local service is `http://localhost:11434`.

## 2. Install and start the backend

Open PowerShell in `KuralAI/apps/api`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` to view the API documentation. Health check: `http://127.0.0.1:8000/health`.

## 3. Add legal PDF documents and index them

Place text-based, authoritative legal PDFs in:

```text
KuralAI/data/raw/legal_documents/
```

For example, use official government or statutory sources and verify the publication/version date. Do not use random summaries as the legal knowledge base.

In a second PowerShell window, from `KuralAI/apps/api` with the virtual environment activated:

```powershell
python ingest.py
```

The script extracts text, splits it into overlapping chunks, generates embeddings with Ollama `all-minilm`, and stores them in `data/processed/chroma_db`.

Scanned image-only PDFs need OCR before this ingestion pipeline can retrieve their text.

## 4. Test the backend

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json" -Body '{"message":"What is the complaint filing time limit under the POSH Act?","language":"English"}'
```

The response contains `answer`, `sources`, and `language`. If no relevant indexed passage is found, KuralAI should say the indexed documents do not contain enough information.

## 5. Start the frontend

Open another PowerShell window in `KuralAI/apps/web`:

```powershell
npm install
$env:NEXT_PUBLIC_API_URL="http://localhost:8000"
npm run dev
```

Open `http://localhost:3000`, then choose **Explore Legal Assistance** or visit `http://localhost:3000/chat`.

## Troubleshooting

- **Ollama connection error:** make sure Ollama is running and both models appear in `ollama list`.
- **No relevant legal passages:** add PDFs to `data/raw/legal_documents/` and run `python ingest.py`.
- **No text extracted:** the PDF may be scanned; OCR it first.
- **Browser CORS error:** add the exact frontend origin to `KURALAI_CORS_ORIGINS`, then restart FastAPI.
- **Chroma dimension error:** do not change embedding models after indexing without rebuilding the Chroma collection using one consistent model. Back up data before deleting/rebuilding the vector store.

## Important limitations

- The current project is a local prototype; it does not include production authentication, authorization, MFA, rate limiting, audit logging, or secure multi-user document access.
- The language selector asks the LLM to answer in the selected language. Translation quality must be evaluated with fluent speakers.
- Similarity thresholds need testing against a labelled evaluation set. Retrieval similarity is not proof that a legal passage is correct or current.
- Source references identify the retrieved PDF, page and chunk. Check the original PDF before relying on a legal statement.
