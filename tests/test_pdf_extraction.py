from src.pdf_loader import extract_text_from_pdf


print("========== PDF EXTRACTION TEST ==========")

file_path = "data/uploads/basic-text.pdf"

try:
    pages = extract_text_from_pdf(file_path)

    print("PDF opened successfully: ✅")
    print("Pages extracted:", len(pages))

    if pages:
        print("Text extraction: ✅")

        for page in pages[:3]:
            print(
                f"Page {page['page']}: "
                f"{len(page['text'])} characters"
            )
    else:
        print("Text extraction: ⚠️ No text found")

except Exception as e:
    print("PDF extraction: ❌")
    print("Error:", e)

print("-----------------------------------------")
print("PDF extraction test completed.")