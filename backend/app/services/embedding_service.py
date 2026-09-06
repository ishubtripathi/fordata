from sentence_transformers import SentenceTransformer # type: ignore

from app.models.chunk import DocumentChunk


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector for a single text.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def generate_chunk_embeddings(
    chunks: list[DocumentChunk],
    batch_size: int = 32,
) -> list[dict]:
    """
    Generate embeddings for document chunks in batches.
    """

    if not chunks:
        return []

    if batch_size <= 0:
        raise ValueError(
            "batch_size must be greater than 0."
        )

    texts = [
        chunk.content
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    embedded_chunks = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):

        embedded_chunks.append({
            "chunk": chunk,
            "embedding": embedding.tolist(),
        })

    return embedded_chunks