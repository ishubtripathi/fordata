from app.models.chunk import DocumentChunk

from app.services.vector_service import (
    store_embeddings,
)

from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)


def setup_test_data():

    chunks = [
        DocumentChunk(
            chunk_id="search-test-1",
            document_id="search.pdf",
            filename="search.pdf",
            file_type="pdf",
            content="StarQ is a document intelligence system.",
            page_number=1,
        ),
        DocumentChunk(
            chunk_id="search-test-2",
            document_id="search.pdf",
            filename="search.pdf",
            file_type="pdf",
            content="StarQ processes PDF and CSV documents.",
            page_number=2,
        ),
        DocumentChunk(
            chunk_id="search-test-3",
            document_id="search.pdf",
            filename="search.pdf",
            file_type="pdf",
            content="StarQ uses semantic search and embeddings.",
            page_number=3,
        ),
    ]

    # Dummy vectors for storage testing
    embedded_chunks = [
        {
            "chunk": chunks[0],
            "embedding": [0.1] * 384,
        },
        {
            "chunk": chunks[1],
            "embedding": [0.2] * 384,
        },
        {
            "chunk": chunks[2],
            "embedding": [0.3] * 384,
        },
    ]

    store_embeddings(embedded_chunks)


def test_similarity_search():

    setup_test_data()

    results = retrieve_relevant_chunks(
        query="How does StarQ process documents?",
        top_k=2,
    )

    assert results is not None

    assert "documents" in results
    assert "metadatas" in results
    assert "distances" in results

    assert len(results["documents"]) == 1

    assert len(results["documents"][0]) == 2

    assert len(results["metadatas"][0]) == 2

    assert len(results["distances"][0]) == 2

    print("Retrieved chunks:", len(results["documents"][0]))
    print("Similarity search: PASSED")


if __name__ == "__main__":

    test_similarity_search()

    print("\n4.6 Similarity Search Test: PASSED")