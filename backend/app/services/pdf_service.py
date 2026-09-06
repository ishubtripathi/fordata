import fitz


PDF_SIGNATURE = b"%PDF-"


def validate_pdf(file_path: str) -> dict:
    """
    Validate a PDF file using its file path.
    """

    try:
        with open(file_path, "rb") as file:
            header = file.read(5)

        if not header.startswith(PDF_SIGNATURE):
            return {
                "valid": False,
                "error": "The uploaded file is not a valid PDF.",
            }

        document = fitz.open(file_path)

        page_count = len(document)

        if page_count == 0:
            document.close()

            return {
                "valid": False,
                "error": "The PDF contains no pages.",
            }

        metadata = document.metadata

        document.close()

        return {
            "valid": True,
            "page_count": page_count,
            "metadata": metadata,
        }

    except Exception:
        return {
            "valid": False,
            "error": "The PDF could not be opened or is corrupted.",
        }


def extract_pdf_text(file_path: str):
    """
    Extract PDF text page by page.
    """

    document = fitz.open(file_path)

    try:
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            image_count = len(
                page.get_images(full=True)
            )

            yield {
                "page_number": page_number,
                "text": text,
                "has_text": bool(text),
                "character_count": len(text),
                "image_count": image_count,
            }

    finally:
        document.close()


def extract_pdf_metadata(file_path: str) -> dict:
    """
    Extract PDF metadata and document statistics.
    """

    document = fitz.open(file_path)

    try:
        metadata = document.metadata

        total_pages = len(document)
        total_images = 0
        total_characters = 0
        pages_with_text = 0
        pages_without_text = 0

        for page in document:

            text = page.get_text("text").strip()

            image_count = len(
                page.get_image_info()
            )

            total_characters += len(text)
            total_images += image_count

            if text:
                pages_with_text += 1
            else:
                pages_without_text += 1

        return {
            "metadata": metadata,
            "statistics": {
                "total_pages": total_pages,
                "total_characters": total_characters,
                "total_images": total_images,
                "pages_with_text": pages_with_text,
                "pages_without_text": pages_without_text,
            },
        }

    finally:
        document.close()