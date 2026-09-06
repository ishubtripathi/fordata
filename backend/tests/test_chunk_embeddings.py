from app.models.chunk import DocumentChunk
from app.services.embedding_service import (
    generate_chunk_embeddings,
)


def test_chunk_embeddings():

    chunks = [
        DocumentChunk(
            chunk_id="chunk-1",
            document_id="test.pdf",
            filename="test.pdf",
            file_type="pdf",
            content="StarQ processes PDF documents.",
            page_number=1,
        ),
        DocumentChunk(
            chunk_id="chunk-2",
            document_id="test.pdf",
            filename="test.pdf",
            file_type="pdf",
            content="StarQ uses semantic search.",
            page_number=2,
        ),
    ]

    result = generate_chunk_embeddings(chunks)

    assert len(result) == 2

    for item in result:

        assert "chunk" in item
        assert "embedding" in item

        assert len(item["embedding"]) == 384

        assert all(
            isinstance(value, float)
            for value in item["embedding"]
        )

    print("Chunks processed:", len(result))
    print("Embedding dimension:", len(result[0]["embedding"]))
    print("4.2 Chunk Embedding Test: PASSED")


if __name__ == "__main__":
    test_chunk_embeddings()