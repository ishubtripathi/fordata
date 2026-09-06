from app.services.rag_service import (
    build_rag_prompt,
)


def test_rag_prompt():

    query = "What is StarQ?"

    context = """
[Source 1: test.pdf, Page 1]
StarQ is a document intelligence system.
It processes PDF and CSV documents.
"""

    prompt = build_rag_prompt(
        query=query,
        context=context,
    )

    assert prompt

    assert "StarQ" in prompt
    assert "What is StarQ?" in prompt
    assert "document intelligence system" in prompt

    assert "ONLY" in prompt
    assert "Do not invent" in prompt

    print("Prompt generated successfully.")
    print("Prompt length:", len(prompt))
    print("5.4 Prompt Builder Test: PASSED")


def test_empty_context():

    prompt = build_rag_prompt(
        query="What is StarQ?",
        context="",
    )

    assert "No relevant information was found." in prompt

    print("Empty context handling: PASSED")


def test_empty_query():

    try:

        build_rag_prompt(
            query="",
            context="Some context.",
        )

        assert False

    except ValueError:
        pass

    print("Empty query handling: PASSED")


if __name__ == "__main__":

    test_rag_prompt()
    test_empty_context()
    test_empty_query()

    print("\n5.4 Prompt Builder Test: PASSED")