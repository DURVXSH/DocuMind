from src.embeddings import create_embeddings
from src.vector_store import search_chunks


question = "What is the candidate's CGPA?"

question_embedding = create_embeddings(
    [question]
)[0]

results = search_chunks(
    question_embedding,
    number_of_results=5,
    source="Durvesh_Res.pdf"
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


print("\nQuestion:", question)

print("\nRetrieved distances:")

for i, distance in enumerate(distances):

    print(
        f"\nChunk {i + 1}"
    )

    print(
        f"Distance: {distance:.4f}"
    )

    print(
        f"Page: {metadatas[i]['page']}"
    )

    print(
        f"Text: {documents[i][:200]}..."
    )