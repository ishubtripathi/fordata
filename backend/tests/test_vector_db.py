from app.services.vector_service import get_collection


def test_vector_database():

    collection = get_collection()

    assert collection is not None
    assert collection.name == "starq_documents"

    print("Collection name:", collection.name)
    print("Collection count:", collection.count())
    print("4.4 Vector Database Test: PASSED")


if __name__ == "__main__":
    test_vector_database()