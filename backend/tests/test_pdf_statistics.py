import fitz

from app.services.pdf_statistics import (
    calculate_pdf_statistics,
)


def create_test_pdf():

    document = fitz.open()

    page1 = document.new_page()

    page1.insert_text(
        (50, 50),
        "StarQ is a document intelligence system.",
    )

    page2 = document.new_page()

    page2.insert_text(
        (50, 50),
        "PDF and CSV files are supported.",
    )

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes


def test_pdf_statistics():

    pdf_bytes = create_test_pdf()

    stats = calculate_pdf_statistics(
        pdf_bytes
    )

    assert stats["page_count"] == 2

    assert stats["text_pages"] == 2

    assert stats["empty_pages"] == 0

    assert stats["total_words"] > 0

    assert stats["total_characters"] > 0

    assert stats["total_images"] == 0

    print("PDF statistics: PASSED")

    print(stats)


def test_empty_pdf_data():

    try:

        calculate_pdf_statistics(b"")

        assert False

    except ValueError:
        pass

    print("Empty PDF handling: PASSED")


if __name__ == "__main__":

    test_pdf_statistics()
    test_empty_pdf_data()

    print("\n6.3 PDF Statistics Test: PASSED")