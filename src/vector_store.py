
import uuid

import chromadb


client = chromadb.PersistentClient(
    path="data/chroma_db"
)


collection = client.get_or_create_collection(
    name="documents"
)


def add_chunks(chunks, embeddings):

    if not chunks:
        return

    source = chunks[0]["source"]

    # Remove existing chunks for this document
    try:
        collection.delete(
            where={
                "source": source
            }
        )
    except Exception:
        pass

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            str(uuid.uuid4())
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "page": chunk["page"],
            "source": chunk["source"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def search_chunks(
    query_embedding,
    number_of_results=3,
    source=None
):

    query_parameters = {
    "query_embeddings": [
        query_embedding.tolist()
    ],
    "n_results": number_of_results,
    "include": [
        "documents",
        "metadatas",
        "distances"
    ]
    }

    # Search only within the selected document
    if source:

        query_parameters["where"] = {
            "source": source
        }

    results = collection.query(
        **query_parameters
    )

    return results
def get_all_sources():

    results = collection.get(
        include=["metadatas"]
    )

    sources = set()

    for metadata in results["metadatas"]:

        if metadata and "source" in metadata:
            sources.add(metadata["source"])

    return sorted(sources)
def delete_document(source):
    if not source:
        return False

    existing = collection.get(
        where={"source": source}
    )

    ids = existing.get("ids", [])

    if not ids:
        return False

    collection.delete(
        ids=ids
    )

    return True
def clear_all_documents():
    existing = collection.get()

    ids = existing.get("ids", [])

    if not ids:
        return False

    collection.delete(
        ids=ids
    )

    return True