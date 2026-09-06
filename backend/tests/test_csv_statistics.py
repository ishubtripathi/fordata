from app.services.csv_statistics import (
    calculate_csv_statistics,
)


def test_csv_statistics():

    csv_data = """Name,City,Salary
Rahul,Jaipur,50000
Amit,Delhi,60000
Priya,,
"""

    stats = calculate_csv_statistics(
        csv_data.encode("utf-8")
    )

    assert stats["row_count"] == 3

    assert stats["column_count"] == 3

    assert stats["columns"] == [
        "Name",
        "City",
        "Salary",
    ]

    assert stats["missing_values"] == 2

    print("CSV statistics: PASSED")
    print(stats)


def test_empty_csv():

    try:

        calculate_csv_statistics(b"")

        assert False

    except ValueError:
        pass

    print("Empty CSV handling: PASSED")


def test_csv_without_header():

    csv_data = "\n"

    try:

        calculate_csv_statistics(
            csv_data.encode("utf-8")
        )

        assert False

    except ValueError:
        pass

    print("CSV header validation: PASSED")


if __name__ == "__main__":

    test_csv_statistics()
    test_empty_csv()
    test_csv_without_header()

    print("\n6.4 CSV Statistics Test: PASSED")