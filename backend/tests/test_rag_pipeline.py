from app.services.rag_service import process_query


def test_rag_pipeline():

    result = process_query(
        query="What is StarQ?",
        top_k=3,
    )

    assert result is not None

    assert result["query"] == "What is StarQ?"

    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0

    assert "retrieved_chunks" in result
    assert "chunk_count" in result
    assert "context" in result

    print("\nQuestion:")
    print(result["query"])

    print("\nAnswer:")
    print(result["answer"])

    print(
        "\nRetrieved chunks:",
        result["chunk_count"],
    )

    print("\n5.5 End-to-End RAG Test: PASSED")


if __name__ == "__main__":
    test_rag_pipeline()