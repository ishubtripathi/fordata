from app.services.content_service import chunk_text


def test_chunking():

    text = (
        "StarQ is a document intelligence system. "
        "It processes PDF and CSV files. "
        "The extracted content is cleaned before chunking. "
        "Chunks are later converted into embeddings. "
        "The embeddings are stored in a vector database. "
        "The retrieval system finds relevant chunks. "
        "The language model uses these chunks to generate answers."
    )

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)
        print(f"Length: {len(chunk)}")

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) > 0

    print("\n3.3 Chunking Test: PASSED")


if __name__ == "__main__":
    test_chunking()