from app.services.content_service import create_document_chunks
from app.services.embedding_service import generate_chunk_embeddings
from app.services.vector_service import store_embeddings
from app.services.retrieval_service import (
    retrieve_relevant_chunks,
    format_retrieval_results,
)


def test_phase4_pipeline():

    pages = [
        {
            "page_number": 1,
            "text": (
                "StarQ is a document intelligence system. "
                "It processes PDF and CSV documents."
            ),
        },
        {
            "page_number": 2,
            "text": (
                "StarQ uses embeddings and vector search "
                "to find relevant information."
            ),
        },
    ]

    # 1. Create chunks
    chunks = create_document_chunks(
        filename="phase4.pdf",
        file_type="pdf",
        content=pages,
        chunk_size=1000,
        chunk_overlap=150,
    )

    assert len(chunks) > 0

    # 2. Generate real embeddings
    embedded_chunks = generate_chunk_embeddings(
        chunks,
        batch_size=2,
    )

    assert len(embedded_chunks) == len(chunks)

    for item in embedded_chunks:
        assert len(item["embedding"]) == 384

    # 3. Store vectors
    stored_count = store_embeddings(
        embedded_chunks
    )

    assert stored_count == len(chunks)

    # 4. Search
    results = retrieve_relevant_chunks(
        query="What does StarQ do?",
        top_k=2,
    )

    assert results["documents"]
    assert results["metadatas"]
    assert results["distances"]

    # 5. Format results
    retrieved = format_retrieval_results(
        results
    )

    assert len(retrieved) > 0

    for item in retrieved:

        assert item["content"]
        assert item["source"]["filename"]
        assert item["distance"] is not None

    print("Chunks created:", len(chunks))
    print("Vectors stored:", stored_count)
    print("Chunks retrieved:", len(retrieved))

    print("\n4.8 Phase 4 Integration Test: PASSED")


if __name__ == "__main__":
    test_phase4_pipeline()