from src.retriever import retrieve_relevant_chunks
from tests.evaluation_questions import evaluation_questions


correct_retrieval = 0
correct_page = 0
correct_unanswerable = 0

answerable_questions = 0
unanswerable_questions = 0

total = len(evaluation_questions)


for item in evaluation_questions:

    question = item["question"]
    expected_topic = item["expected_topic"]
    expected_page = item["expected_page"]
    answerable = item["answerable"]

    results = retrieve_relevant_chunks(
        question,
        number_of_results=5,
        source="Durvesh_Res.pdf"
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # --------------------------------
    # Answerable question
    # --------------------------------

    if answerable:

        answerable_questions += 1

        topic_found = any(
            expected_topic.lower()
            in document.lower()
            for document in documents
        )

        page_found = any(
            metadata["page"] == expected_page
            for metadata in metadatas
        )

        if topic_found:

            correct_retrieval += 1
            retrieval_status = "✅"

        else:

            retrieval_status = "❌"

        if page_found:

            correct_page += 1
            page_status = "✅"

        else:

            page_status = "❌"

        print(
            f"\nQuestion: {question}"
        )

        print(
            f"Type: Answerable"
        )

        print(
            f"Retrieval: {retrieval_status} "
            f"Expected: {expected_topic}"
        )

        print(
            f"Page: {page_status} "
            f"Expected: {expected_page}"
        )

        print(
            "Retrieved pages:",
            [
                metadata["page"]
                for metadata in metadatas
            ]
        )

    # --------------------------------
    # Unanswerable question
    # --------------------------------

    else:

        unanswerable_questions += 1

        if not documents:

            correct_unanswerable += 1

            unanswerable_status = "✅"

        else:

            unanswerable_status = "❌"

        print(
            f"\nQuestion: {question}"
        )

        print(
            f"Type: Unanswerable"
        )

        print(
            f"Hallucination Protection: "
            f"{unanswerable_status}"
        )

        print(
            "Retrieved chunks:",
            len(documents)
        )

    print("-" * 60)


# --------------------------------
# Calculate Results
# --------------------------------

if answerable_questions > 0:

    retrieval_accuracy = (
        correct_retrieval /
        answerable_questions
    ) * 100

    page_accuracy = (
        correct_page /
        answerable_questions
    ) * 100

else:

    retrieval_accuracy = 0
    page_accuracy = 0


if unanswerable_questions > 0:

    hallucination_protection = (
        correct_unanswerable /
        unanswerable_questions
    ) * 100

else:

    hallucination_protection = 0


# --------------------------------
# Final Results
# --------------------------------

print(
    "\n========== EVALUATION RESULTS =========="
)

print(
    f"Retrieval Accuracy: "
    f"{retrieval_accuracy:.1f}%"
)

print(
    f"Page Accuracy: "
    f"{page_accuracy:.1f}%"
)

print(
    f"Hallucination Protection: "
    f"{hallucination_protection:.1f}%"
)

print(
    f"Answerable Questions: "
    f"{answerable_questions}"
)

print(
    f"Unanswerable Questions: "
    f"{unanswerable_questions}"
) 