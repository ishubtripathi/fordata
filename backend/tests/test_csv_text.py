from app.services.content_service import prepare_csv_content


def test_csv_text_representation():

    rows = [
        {
            "name": "Rahul",
            "age": "22",
            "city": "Jaipur",
            "profession": "Developer",
        },
        {
            "name": "Aman",
            "age": "",
            "city": "Delhi",
            "profession": "Tester",
        },
    ]

    chunks = prepare_csv_content(
        "employees.csv",
        rows,
    )

    assert len(chunks) == 2

    first = chunks[0]

    assert "name: Rahul" in first.content
    assert "age: 22" in first.content
    assert "city: Jaipur" in first.content
    assert "profession: Developer" in first.content

    second = chunks[1]

    assert "name: Aman" in second.content
    assert "city: Delhi" in second.content
    assert "age:" not in second.content

    assert first.row_number == 1
    assert second.row_number == 2

    print("CSV text representation: PASSED")


if __name__ == "__main__":
    test_csv_text_representation()

    print("\n3.6 CSV Text Representation Test: PASSED")