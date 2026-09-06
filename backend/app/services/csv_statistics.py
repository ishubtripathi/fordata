import csv
import io


def calculate_csv_statistics(
    file_bytes: bytes,
) -> dict:
    """
    Calculate statistics for a CSV document.
    """

    if not file_bytes:
        raise ValueError(
            "CSV data cannot be empty."
        )

    try:
        text = file_bytes.decode(
            "utf-8-sig"
        )
    except UnicodeDecodeError:
        text = file_bytes.decode(
            "utf-8",
            errors="replace",
        )

    reader = csv.DictReader(
        io.StringIO(text)
    )

    columns = reader.fieldnames or []

    if not columns:
        raise ValueError(
            "CSV does not contain a header row."
        )

    rows = list(reader)

    row_count = len(rows)
    column_count = len(columns)

    missing_values = 0

    for row in rows:
        for column in columns:
            value = row.get(column)

            if value is None or not value.strip():
                missing_values += 1

    return {
        "row_count": row_count,
        "column_count": column_count,
        "columns": columns,
        "missing_values": missing_values,
    }