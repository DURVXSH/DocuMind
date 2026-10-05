from src.text_splitter import split_text


print("========== LARGE DOCUMENT TEST ==========")

large_text = "This is a sample document sentence. " * 10000

pages = [
    {
        "page": 1,
        "text": large_text
    }
]

chunks = split_text(
    pages,
    "large_test.pdf"
)

print("Original characters:", len(large_text))
print("Chunks created:", len(chunks))

if len(chunks) > 10:
    print("Large document chunking: ✅")
else:
    print("Large document chunking: ❌")

if all(len(chunk["text"]) <= 700 for chunk in chunks):
    print("Chunk size limit: ✅")
else:
    print("Chunk size limit: ❌")

print("-----------------------------------------")
print("Large document test completed.")