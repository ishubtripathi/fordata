from app.services.content_service import (
    create_document_chunks,
)


def test_pdf_chunks():

    pages = [
        {
            "page_number": 1,
            "text": "StarQ processes documents.",
        },
        {
            "page_number": 2,
            "text": "StarQ uses RAG technology.",
        },
    ]

    chunks = create_document_chunks(
        filename="test.pdf",
        file_type="pdf",
        content=pages,
    )

    assert len(chunks) == 2
    assert chunks[0].file_type == "pdf"
    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 2

    print("PDF unified chunks: PASSED")


def test_csv_chunks():

    rows = [
        {
            "name": "Rahul",
            "city": "Jaipur",
        },
        {
            "name": "Aman",
            "city": "Delhi",
        },
    ]

    chunks = create_document_chunks(
        filename="test.csv",
        file_type="csv",
        content=rows,
    )

    assert len(chunks) == 2
    assert chunks[0].file_type == "csv"
    assert chunks[0].row_number == 1
    assert chunks[1].row_number == 2

    print("CSV unified chunks: PASSED")


def test_invalid_file_type():

    try:

        create_document_chunks(
            filename="test.txt",
            file_type="txt",
            content=[],
        )

        assert False

    except ValueError:
        pass

    print("Invalid file type: PASSED")


if __name__ == "__main__":

    test_pdf_chunks()
    test_csv_chunks()
    test_invalid_file_type()

    print("\n3.7 Unified Chunk Pipeline Test: PASSED")