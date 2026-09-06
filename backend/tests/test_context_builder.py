from app.services.rag_service import build_context


def test_pdf_context():

    chunks = [
        {
            "content": "StarQ processes PDF documents.",
            "source": {
                "filename": "test.pdf",
                "file_type": "pdf",
                "page_number": 5,
                "row_number": None,
            },
        },
        {
            "content": "StarQ uses vector search.",
            "source": {
                "filename": "test.pdf",
                "file_type": "pdf",
                "page_number": 8,
                "row_number": None,
            },
        },
    ]

    context = build_context(chunks)

    assert context

    assert "[Source 1: test.pdf, Page 5]" in context
    assert "[Source 2: test.pdf, Page 8]" in context

    assert "StarQ processes PDF documents." in context
    assert "StarQ uses vector search." in context

    print("PDF context: PASSED")


def test_csv_context():

    chunks = [
        {
            "content": "name: Rahul. city: Jaipur.",
            "source": {
                "filename": "employees.csv",
                "file_type": "csv",
                "page_number": None,
                "row_number": 3,
            },
        }
    ]

    context = build_context(chunks)

    assert "[Source 1: employees.csv, Row 3]" in context

    assert "name: Rahul. city: Jaipur." in context

    print("CSV context: PASSED")


def test_empty_context():

    context = build_context([])

    assert context == ""

    print("Empty context: PASSED")


if __name__ == "__main__":

    test_pdf_context()
    test_csv_context()
    test_empty_context()

    print("\n5.2 Context Builder Test: PASSED")