from app.services.document_service import (
    build_document_overview,
)


def test_pdf_overview():

    overview = build_document_overview(
        filename="sample.pdf",
        file_type="pdf",
        file_size=102400,
        metadata={
            "page_count": 102,
            "has_text": True,
            "image_count": 25,
        },
    )

    assert overview["filename"] == "sample.pdf"
    assert overview["file_type"] == "pdf"
    assert overview["file_size_bytes"] == 102400

    assert overview["metadata"]["page_count"] == 102
    assert overview["metadata"]["has_text"] is True
    assert overview["metadata"]["image_count"] == 25

    print("PDF document overview: PASSED")


def test_csv_overview():

    overview = build_document_overview(
        filename="data.csv",
        file_type="csv",
        file_size=50000,
        metadata={
            "row_count": 500,
            "column_count": 8,
        },
    )

    assert overview["filename"] == "data.csv"
    assert overview["file_type"] == "csv"

    assert overview["metadata"]["row_count"] == 500
    assert overview["metadata"]["column_count"] == 8

    print("CSV document overview: PASSED")


if __name__ == "__main__":

    test_pdf_overview()
    test_csv_overview()

    print("\n6.1 Document Overview Test: PASSED")