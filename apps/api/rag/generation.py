
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"


def generate_answer(question: str, retrieved_chunks: list):

    if not retrieved_chunks:
        return (
        "The available legal documents do not provide "
        "sufficient information to answer this question. "
        "Please consult an appropriate legal professional "
        "or refer to an authoritative legal source."
        )

    # Build legal context from retrieved passages
    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        context_parts.append(
            f"""
LEGAL SOURCE {index}
Document: {chunk['source']}
Page: {chunk['page']}
Section/Chunk: {chunk['chunk']}

Content:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are KuralAI, an Indian legal information assistant.

Your task is to explain Indian legal information in
simple, clear language.

STRICT RULES:

1. Answer using ONLY the supplied legal context.
2. Do not use your pretrained knowledge to invent legal facts.
3. Never invent sections, acts, dates, penalties or procedures.
4. If the context does not answer the question, clearly say:
   "The available legal documents do not provide sufficient
   information to answer this question."
5. Preserve the actual meaning of the legal provision.
6. Explain complex legal terminology in simple language.
7. Do not provide fabricated legal advice.
8. Keep the answer relevant to the user's question.

RETRIEVED LEGAL CONTEXT:

{context}

USER QUESTION:

{question}

Write a concise, accurate answer based only on the
retrieved legal context.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a careful legal information "
                            "assistant. Never fabricate legal facts."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_ctx": 4096
                }
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"].strip()

    except requests.exceptions.RequestException as error:

        print("Ollama connection error:", error)

        return (
            "KuralAI is currently unable to generate a response. "
            "Please try again later."
        )
