
from rag.retrieval import retrieve_relevant_chunks
from rag.llm import generate_answer


def run_retrieval_smoke_test():

    questions = [
        "What is sexual harassment at the workplace?",
    "Who is responsible for handling workplace complaints?",
    "What is the time limit for filing a complaint?",

    # Irrelevant questions
    "What are the legal provisions relating to space exploration?",
    "Explain quantum computing.",
    "What are the tax rules for cryptocurrency?"
    ]

    for question in questions:

        print("\n" + "=" * 75)
        print("QUESTION:", question)
        print("=" * 75)

        results = retrieve_relevant_chunks(
            query=question,
            top_k=4
        )

        if not results:
            print("No documents available for retrieval.")
            continue

        print("\nRETRIEVED LEGAL PASSAGES:")

        for index, result in enumerate(results, start=1):

            print(f"\nRESULT {index}")

            print("Source:", result["source"])
            print("Page:", result["page"])
            print("Chunk:", result["chunk"])
            print("Distance:", round(result["distance"], 4))
            print("Content:", result["text"][:350])

        print("\nGENERATED KURALAI RESPONSE:")

        answer = generate_answer(
            question=question,
            retrieved_chunks=results,
            language="English"
        )

        print(answer)


if __name__ == "__main__":
    run_retrieval_smoke_test()

