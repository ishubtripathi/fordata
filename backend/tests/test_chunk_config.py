from app.services.content_service import chunk_text
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


def test_default_configuration():

    assert CHUNK_SIZE == 1000
    assert CHUNK_OVERLAP == 150

    print("Default configuration: PASSED")


def test_invalid_configuration():

    try:
        chunk_text(
            "This is test text.",
            chunk_size=100,
            chunk_overlap=100,
        )

        assert False

    except ValueError:
        pass

    print("Invalid configuration: PASSED")


if __name__ == "__main__":

    test_default_configuration()
    test_invalid_configuration()

    print("\n3.5 Chunk Configuration Test: PASSED")