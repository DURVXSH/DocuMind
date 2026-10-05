def split_text(pages, source):

    chunks = []

    chunk_size = 700
    overlap = 150

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page": page_number,
                "source": source
            })

            start += chunk_size - overlap

    return chunks