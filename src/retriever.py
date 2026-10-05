import re

from src.embeddings import create_embeddings
from src.vector_store import search_chunks


def get_question_keywords(question):
    stop_words = {
        "what", "is", "are", "the", "a", "an", "of",
        "does", "do", "did", "can", "could", "would",
        "should", "how", "why", "when", "where",
        "who", "which", "and", "or", "to", "in",
        "on", "for", "with", "has", "have", "had",
        "candidate"
    }

    words = re.findall(
        r"\b[a-zA-Z0-9.]+\b",
        question.lower()
    )

    return [
        word
        for word in words
        if word not in stop_words and len(word) > 2
    ]


def retrieve_relevant_chunks(
    question,
    number_of_results=5,
    source=None
):
    question_embedding = create_embeddings([question])[0]

    results = search_chunks(
        question_embedding,
        number_of_results,
        source
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    question_keywords = get_question_keywords(question)

    relevant_indexes = []

    for index, distance in enumerate(distances):

        # Very weak semantic matches are rejected
        if distance >= 1.8:
            continue

        document_text = documents[index].lower()

        keyword_found = any(
            keyword in document_text
            for keyword in question_keywords
        )

        # Accept if:
        # 1. A question keyword appears in the chunk
        # OR
        # 2. The semantic match is very strong
        if keyword_found or distance < 1.65:
            relevant_indexes.append(index)

    results["documents"][0] = [
        documents[index]
        for index in relevant_indexes
    ]

    results["metadatas"][0] = [
        metadatas[index]
        for index in relevant_indexes
    ]

    results["distances"][0] = [
        distances[index]
        for index in relevant_indexes
    ]

    return results