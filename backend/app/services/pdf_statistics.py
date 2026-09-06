import fitz


def calculate_pdf_statistics(
    file_bytes: bytes,
) -> dict:
    """
    Calculate statistics for a PDF document.
    """

    if not file_bytes:
        raise ValueError("PDF data cannot be empty.")

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf",
    )

    page_count = len(document)

    total_characters = 0
    total_words = 0
    text_pages = 0
    empty_pages = 0
    total_images = 0

    for page in document:

        text = page.get_text("text").strip()

        if text:
            text_pages += 1
        else:
            empty_pages += 1

        total_characters += len(text)
        total_words += len(text.split())

        total_images += len(
            page.get_images(full=True)
        )

    document.close()

    return {
        "page_count": page_count,
        "text_pages": text_pages,
        "empty_pages": empty_pages,
        "total_words": total_words,
        "total_characters": total_characters,
        "total_images": total_images,
    }