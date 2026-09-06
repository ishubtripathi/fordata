from app.services.content_service import (
    prepare_pdf_content,
    prepare_csv_content,
)


def test_pdf_metadata():

    pages = [
        {
            "page_number": 5,
            "text": "StarQ processes documents.",
        }
    ]

    chunks = prepare_pdf_content(
        "test.pdf",
        pages,
        chunk_size=100,
        chunk_overlap=20,
    )

    chunk = chunks[0]

    assert chunk.filename == "test.pdf"
    assert chunk.file_type == "pdf"
    assert chunk.page_number == 5
    assert chunk.chunk_id


def test_csv_metadata():

    rows = [
        {
            "name": "Rahul",
            "age": "22",
            "city": "Jaipur",
        }
    ]

    chunks = prepare_csv_content(
        "test.csv",
        rows,
    )

    chunk = chunks[0]

    assert chunk.filename == "test.csv"
    assert chunk.file_type == "csv"
    assert chunk.row_number == 1
    assert chunk.chunk_id


if __name__ == "__main__":

    test_pdf_metadata()
    test_csv_metadata()

    print("3.4 Chunk Metadata Test: PASSED")