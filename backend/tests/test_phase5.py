from app.services.rag_service import process_query


def test_phase5_rag_pipeline():

    result = process_query(
        query="What is StarQ?",
        top_k=5,
    )

    # Basic response validation
    assert result is not None

    assert result["query"] == "What is StarQ?"

    # Answer validation
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"].strip()) > 0

    # Retrieval validation
    assert "retrieved_chunks" in result
    assert "chunk_count" in result

    # Context validation
    assert "context" in result

    # Sources validation
    assert "sources" in result
    assert isinstance(result["sources"], list)

    print("\n========== PHASE 5 TEST ==========")

    print("Query:")
    print(result["query"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieved chunks:")
    print(result["chunk_count"])

    print("\nSources:")
    for source in result["sources"]:
        print(
            f"- {source['filename']} | "
            f"Page: {source['page_number']} | "
            f"Distance: {source['distance']}"
        )

    print("\n5.9 Phase 5 End-to-End Test: PASSED")


if __name__ == "__main__":
    test_phase5_rag_pipeline()