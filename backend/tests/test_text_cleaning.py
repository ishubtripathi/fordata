from app.services.content_service import clean_text


def test_clean_text():

    raw_text = (
        "Hello    World\n\n\n\n"
        "This   is   StarQ.   "
    )

    cleaned_text = clean_text(raw_text)

    print("Original:")
    print(repr(raw_text))

    print("\nCleaned:")
    print(repr(cleaned_text))

    assert cleaned_text == "Hello World\n\nThis is StarQ."


if __name__ == "__main__":
    test_clean_text()
    print("\n3.2 Text Cleaning Test: PASSED")