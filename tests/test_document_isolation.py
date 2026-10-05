from src.retriever import retrieve_relevant_chunks


test_cases = [

    {
        "question": "What is the candidate's CGPA?",
        "source": "Durvesh_Res.pdf"
    },

    {
        "question": "What is ReactJS?",
        "source": "ReactJS_Test.docx"
    }

]


for test in test_cases:

    question = test["question"]
    expected_source = test["source"]

    results = retrieve_relevant_chunks(
        question,
        number_of_results=5,
        source=expected_source
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    sources = [
        metadata["source"]
        for metadata in metadatas
    ]

    print("\nQuestion:", question)
    print("Expected source:", expected_source)
    print("Retrieved sources:", sources)

    if sources and all(
        source == expected_source
        for source in sources
    ):

        print("✅ PASS — Document isolation is working")

    else:

        print("❌ FAIL — Wrong document retrieved")

    print("-" * 60)