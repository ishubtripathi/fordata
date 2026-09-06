from app.services.rag_service import build_sources


def test_pdf_sources():

    chunks = [
        {
            "content": "StarQ processes PDF documents.",
            "source": {
                "filename": "report.pdf",
                "file_type": "pdf",
                "page_number": 12,
                "row_number": None,
            },
            "distance": 0.15,
        },
        {
            "content": "StarQ uses vector search.",
            "source": {
                "filename": "report.pdf",
                "file_type": "pdf",
                "page_number": 25,
                "row_number": None,
            },
            "distance": 0.22,
        },
    ]

    sources = build_sources(chunks)

    assert len(sources) == 2

    assert sources[0]["filename"] == "report.pdf"
    assert sources[0]["file_type"] == "pdf"
    assert sources[0]["page_number"] == 12
    assert sources[0]["distance"] == 0.15

    assert sources[1]["page_number"] == 25

    print("PDF source handling: PASSED")


def test_csv_sources():

    chunks = [
        {
            "content": "Name: Rahul, City: Jaipur",
            "source": {
                "filename": "employees.csv",
                "file_type": "csv",
                "page_number": None,
                "row_number": 17,
            },
            "distance": 0.09,
        }
    ]

    sources = build_sources(chunks)

    assert len(sources) == 1

    assert sources[0]["filename"] == "employees.csv"
    assert sources[0]["file_type"] == "csv"
    assert sources[0]["row_number"] == 17
    assert sources[0]["distance"] == 0.09

    print("CSV source handling: PASSED")


def test_empty_sources():

    sources = build_sources([])

    assert sources == []

    print("Empty source handling: PASSED")


if __name__ == "__main__":

    test_pdf_sources()
    test_csv_sources()
    test_empty_sources()

    print("\n5.6 Source Handling Test: PASSED")