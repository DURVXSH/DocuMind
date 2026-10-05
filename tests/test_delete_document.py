from src.vector_store import (
    get_all_sources,
    delete_document
)


print("========== DELETE DOCUMENT TEST ==========")

print("\nDocuments before deletion:")
print(get_all_sources())

test_document = "ReactJS_Test.docx"

print(f"\nDeleting: {test_document}")

deleted = delete_document(test_document)

if deleted:
    print("Delete operation: ✅")
else:
    print("Delete operation: ❌")


print("\nDocuments after deletion:")
print(get_all_sources())

if test_document not in get_all_sources():
    print("Document removed from ChromaDB: ✅")
else:
    print("Document still exists: ❌")

print("-------------------------------------------")
print("Delete document test completed.")