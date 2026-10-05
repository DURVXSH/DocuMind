from src.vector_store import (
    get_all_sources,
    clear_all_documents
)


print("========== CLEAR ALL DOCUMENTS TEST ==========")

print("\nDocuments before clearing:")
print(get_all_sources())

cleared = clear_all_documents()

if cleared:
    print("\nClear operation: ✅")
else:
    print("\nClear operation: ⚠️ No documents found")


print("\nDocuments after clearing:")
print(get_all_sources())

if len(get_all_sources()) == 0:
    print("All documents removed from ChromaDB: ✅")
else:
    print("Documents still exist: ❌")

print("----------------------------------------------")
print("Clear all documents test completed.")