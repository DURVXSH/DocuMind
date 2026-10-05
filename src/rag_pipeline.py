from src.retriever import retrieve_relevant_chunks
from src.llm import ask_gemini


def answer_question(
    question,
    conversation_history="",
    source=None
):

    results = retrieve_relevant_chunks(
        question,
        number_of_results=5,
        source=source
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        return (
            "I could not find this information in the document.",
            []
        )

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"[Source: {metadata['source']}, "
            f"Page: {metadata['page']}]\n"
            f"{document}"
        )

    context = "\n\n".join(context_parts)

    answer = ask_gemini(
        question,
        context,
        conversation_history
    )

    sources = []

    for metadata in metadatas:

        source_info = {
            "source": metadata["source"],
            "page": metadata["page"]
        }

        if source_info not in sources:
            sources.append(source_info)

    return answer, sources