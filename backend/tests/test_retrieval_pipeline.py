from app.services.retrieval_service import (
    format_retrieval_results,
)


def test_format_pdf_results():

    results = {
        "documents": [
            [
                "StarQ processes PDF documents.",
                "StarQ uses semantic search.",
            ]
        ],
        "metadatas": [
            [
                {
                    "filename": "test.pdf",
                    "file_type": "pdf",
                    "page_number": 5,
                },
                {
                    "filename": "test.pdf",
                    "file_type": "pdf",
                    "page_number": 8,
                },
            ]
        ],
        "distances": [
            [0.12, 0.25]
        ],
    }

    formatted = format_retrieval_results(
        results
    )

    assert len(formatted) == 2

    assert (
        formatted[0]["content"]
        == "StarQ processes PDF documents."
    )

    assert (
        formatted[0]["source"]["filename"]
        == "test.pdf"
    )

    assert (
        formatted[0]["source"]["page_number"]
        == 5
    )

    assert formatted[0]["distance"] == 0.12

    print("PDF retrieval formatting: PASSED")


def test_format_csv_results():

    results = {
        "documents": [
            [
                "name: Rahul. city: Jaipur."
            ]
        ],
        "metadatas": [
            [
                {
                    "filename": "employees.csv",
                    "file_type": "csv",
                    "row_number": 3,
                }
            ]
        ],
        "distances": [
            [0.08]
        ],
    }

    formatted = format_retrieval_results(
        results
    )

    assert len(formatted) == 1

    assert (
        formatted[0]["source"]["filename"]
        == "employees.csv"
    )

    assert (
        formatted[0]["source"]["row_number"]
        == 3
    )

    assert formatted[0]["distance"] == 0.08

    print("CSV retrieval formatting: PASSED")


def test_empty_results():

    formatted = format_retrieval_results({})

    assert formatted == []

    print("Empty results handling: PASSED")


if __name__ == "__main__":

    test_format_pdf_results()
    test_format_csv_results()
    test_empty_results()

    print("\n4.7 Retrieval Pipeline Test: PASSED")