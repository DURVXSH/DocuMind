from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def extract_text_from_docx(file_path):

    document = Document(file_path)

    pages = []

    text_parts = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text_parts.append(
                paragraph.text
            )

    if text_parts:

        pages.append({
            "page": 1,
            "text": "\n".join(text_parts)
        })

    return pages