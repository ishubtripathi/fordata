from app.models.chunk import DocumentChunk

from app.services.vector_service import (
    get_collection,
    store_embeddings,
)


def test_vector_storage():

    chunks = [
        DocumentChunk(
            chunk_id="test-chunk-1",
            document_id="test.pdf",
            filename="test.pdf",
            file_type="pdf",
            content="StarQ processes PDF documents.",
            page_number=1,
        ),
        DocumentChunk(
            chunk_id="test-chunk-2",
            document_id="test.pdf",
            filename="test.pdf",
            file_type="pdf",
            content="StarQ uses semantic search.",
            page_number=2,
        ),
    ]

    embedded_chunks = [
        {
            "chunk": chunks[0],
            "embedding": [0.1] * 384,  #not real embeddings nahi hai. Sirf ChromaDB storage test ke liye dummy 384-dimensional vectors hain.
        },
        {
            "chunk": chunks[1],
            "embedding": [0.2] * 384, #not real embeddings nahi hai. Sirf ChromaDB storage test ke liye dummy 384-dimensional vectors hain.
        },
    ]

    stored_count = store_embeddings(
        embedded_chunks
    )

    assert stored_count == 2

    collection = get_collection()

    result = collection.get(
        ids=[
            "test-chunk-1",
            "test-chunk-2",
        ],
        include=[
            "documents",
            "metadatas",
            "embeddings",
        ],
    )

    assert len(result["ids"]) == 2

    assert result["documents"][0] is not None

    assert result["metadatas"][0]["filename"] == "test.pdf"

    print("Stored vectors:", stored_count)
    print("Collection count:", collection.count())
    print("4.5 Vector Storage Test: PASSED")


if __name__ == "__main__":
    test_vector_storage()