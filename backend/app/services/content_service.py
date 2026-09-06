from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.models.chunk import DocumentChunk
import uuid
import re

# pdf preparation
def prepare_pdf_content(
    filename: str,
    pages: list[dict],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[DocumentChunk]:

    chunks = []

    for page in pages:

        text = clean_text(page["text"])

        if not text:
            continue

        page_chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk in page_chunks:

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    document_id=filename,
                    filename=filename,
                    file_type="pdf",
                    content=chunk,
                    page_number=page["page_number"],
                )
            )

    return chunks

# csv preparation

def prepare_csv_content(
    filename: str,
    rows: list[dict],
) -> list[DocumentChunk]:

    chunks = []

    for row_number, row in enumerate(rows, start=1):

        content_parts = []

        for key, value in row.items():

            if value is None or str(value).strip() == "":
                continue

            content_parts.append(
                f"{key}: {str(value).strip()}"
            )

        content = ". ".join(content_parts)

        if not content:
            continue

        chunks.append(
            DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                document_id=filename,
                filename=filename,
                file_type="csv",
                content=content,
                row_number=row_number,
            )
        )

    return chunks


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted document text.
    """

    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if len(current_chunk) + len(sentence) + 1 <= chunk_size:

            current_chunk = (
                f"{current_chunk} {sentence}"
            ).strip()

        else:

            if current_chunk:
                chunks.append(current_chunk)

            overlap_text = current_chunk[-chunk_overlap:]

            current_chunk = (
                f"{overlap_text} {sentence}"
            ).strip()

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# this function is prevent the seperate processing call of pdf and csv, Ek common function dono ko DocumentChunk format mein convert karega.

def create_document_chunks(
    filename: str,
    file_type: str,
    content,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """
    Convert PDF or CSV content into a unified list
    of DocumentChunk objects.
    """

    if file_type == "pdf":

        return prepare_pdf_content(
            filename=filename,
            pages=content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if file_type == "csv":

        return prepare_csv_content(
            filename=filename,
            rows=content,
        )

    raise ValueError(
        f"Unsupported file type: {file_type}"
    )