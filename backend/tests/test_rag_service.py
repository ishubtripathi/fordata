from app.services.rag_service import process_query


def test_process_query():

    result = process_query(
        query="What is StarQ?",
        top_k=2,
    )

    assert result["query"] == "What is StarQ?"

    assert "retrieved_chunks" in result

    assert "chunk_count" in result

    assert result["chunk_count"] <= 2

    print("Query:", result["query"])
    print("Retrieved chunks:", result["chunk_count"])
    print("5.1 RAG Query Service Test: PASSED")


if __name__ == "__main__":
    test_process_query()