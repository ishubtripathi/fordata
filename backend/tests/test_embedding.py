from app.services.embedding_service import generate_embedding


def test_embedding():

    text = "StarQ is a document intelligence system."

    embedding = generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384 # ye specifically all-MiniLM-L6-v2 ka output dimension hai.
    assert all(isinstance(value, float) for value in embedding)

    print("Embedding dimensions:", len(embedding))
    print("4.1 Embedding Test: PASSED")


if __name__ == "__main__":
    test_embedding()