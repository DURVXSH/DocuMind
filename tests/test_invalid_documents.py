from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text


print("========== INVALID DOCUMENT TEST ==========")

# Test 1: Empty pages
empty_pages = []

chunks = split_text(
    empty_pages,
    "empty.pdf"
)

if not chunks:
    print("Empty document handling: ✅")
else:
    print("Empty document handling: ❌")


# Test 2: Empty extracted page
empty_page = [
    {
        "page": 1,
        "text": ""
    }
]

chunks = split_text(
    empty_page,
    "empty_page.pdf"
)

if not chunks:
    print("Empty page handling: ✅")
else:
    print("Empty page handling: ❌")


print("--------------------------------------------")
print("Invalid document tests completed.")