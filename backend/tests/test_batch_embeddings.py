from app.models.chunk import DocumentChunk
from app.services.embedding_service import (
    generate_chunk_embeddings,
)


def test_batch_embeddings():

    chunks = [
        DocumentChunk(
            chunk_id=f"chunk-{i}",
            document_id="test.pdf",
            filename="test.pdf",
            file_type="pdf",
            content=f"StarQ document content number {i}.",
            page_number=i,
        )
        for i in range(1, 6)
    ]

    result = generate_chunk_embeddings(
        chunks,
        batch_size=2,
    )

    assert len(result) == 5

    for index, item in enumerate(result):

        assert item["chunk"].chunk_id == f"chunk-{index + 1}"

        assert len(item["embedding"]) == 384

        assert all(
            isinstance(value, float)
            for value in item["embedding"]
        )

    print("Chunks processed:", len(result))
    print("Embedding dimension:", len(result[0]["embedding"]))
    print("4.3 Batch Embedding Test: PASSED")


if __name__ == "__main__":
    test_batch_embeddings()