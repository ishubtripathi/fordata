from app.services.insight_service import (
    build_insight_prompt,
)


def test_pdf_insight_prompt():

    text = """
    StarQ is a document intelligence platform.
    It supports PDF and CSV processing.
    The system uses RAG for question answering.
    """

    prompt = build_insight_prompt(
        document_text=text,
        file_type="pdf",
    )

    assert prompt
    assert "PDF" in prompt
    assert "StarQ" in prompt
    assert "key_points" in prompt
    assert "summary" in prompt
    assert "entities" in prompt
    assert "topics" in prompt
    assert "Do not invent information" in prompt

    print("PDF insight prompt: PASSED")


def test_csv_insight_prompt():

    text = """
    Name,City,Salary
    Rahul,Jaipur,50000
    Amit,Delhi,60000
    """

    prompt = build_insight_prompt(
        document_text=text,
        file_type="csv",
    )

    assert "CSV" in prompt
    assert "Salary" in prompt
    assert "key_points" in prompt

    print("CSV insight prompt: PASSED")


def test_empty_document():

    try:

        build_insight_prompt(
            document_text="",
            file_type="pdf",
        )

        assert False

    except ValueError:
        pass

    print("Empty document handling: PASSED")


if __name__ == "__main__":

    test_pdf_insight_prompt()
    test_csv_insight_prompt()
    test_empty_document()

    print("\n6.2 Important Information Test: PASSED")