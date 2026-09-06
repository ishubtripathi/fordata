from app.services.content_service import (
    clean_text,
    chunk_text,
    create_document_chunks,
)


def test_pdf_pipeline():

    pages = [
        {
            "page_number": 1,
            "text": (
                "StarQ is a document intelligence system. "
                "It processes PDF documents. "
                "The extracted content is cleaned before "
                "being divided into smaller chunks."
            ),
        }
    ]

    # Step 1: Cleaning
    cleaned = clean_text(pages[0]["text"])

    assert cleaned
    assert "  " not in cleaned

    # Step 2: Chunking
    chunks = chunk_text(
        cleaned,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) > 0

    # Step 3: Unified chunks
    document_chunks = create_document_chunks(
        filename="test.pdf",
        file_type="pdf",
        content=pages,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(document_chunks) > 0

    for chunk in document_chunks:

        assert chunk.chunk_id
        assert chunk.filename == "test.pdf"
        assert chunk.file_type == "pdf"
        assert chunk.page_number == 1
        assert chunk.content


def test_csv_pipeline():

    rows = [
        {
            "name": "Rahul",
            "age": "22",
            "city": "Jaipur",
        },
        {
            "name": "Aman",
            "age": "24",
            "city": "Delhi",
        },
    ]

    document_chunks = create_document_chunks(
        filename="test.csv",
        file_type="csv",
        content=rows,
    )

    assert len(document_chunks) == 2

    for chunk in document_chunks:

        assert chunk.chunk_id
        assert chunk.filename == "test.csv"
        assert chunk.file_type == "csv"
        assert chunk.row_number is not None
        assert chunk.content


if __name__ == "__main__":

    test_pdf_pipeline()
    print("PDF pipeline: PASSED")

    test_csv_pipeline()
    print("CSV pipeline: PASSED")

    print("\nPhase 3 Final Validation: PASSED")