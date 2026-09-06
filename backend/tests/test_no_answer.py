from app.services.rag_service import (
    build_sources,
)


def test_no_answer_sources():

    sources = build_sources([])

    assert sources == []

    print("No-answer source handling: PASSED")


def test_low_relevance_filtering():

    from app.services.retrieval_service import (
        format_retrieval_results,
    )

    results = {
        "documents": [
            [
                "Relevant information.",
                "Unrelated information.",
            ]
        ],
        "metadatas": [
            [
                {
                    "filename": "test.pdf",
                    "file_type": "pdf",
                    "page_number": 1,
                },
                {
                    "filename": "test.pdf",
                    "file_type": "pdf",
                    "page_number": 2,
                },
            ]
        ],
        "distances": [
            [
                0.20,
                0.90,
            ]
        ],
    }

    filtered = format_retrieval_results(
        results,
        distance_threshold=0.70,
    )

    assert len(filtered) == 1

    assert (
        filtered[0]["content"]
        == "Relevant information."
    )

    print("Low-relevance filtering: PASSED")


if __name__ == "__main__":

    test_no_answer_sources()
    test_low_relevance_filtering()

    print("\n5.7 No-Answer Protection Test: PASSED")