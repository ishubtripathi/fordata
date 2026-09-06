import csv


def validate_csv(file_path: str) -> dict:
    """
    Validate CSV structure and collect basic information.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            sample = file.read(8192)

            if not sample.strip():
                return {
                    "valid": False,
                    "error": "The CSV file is empty.",
                }

            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                dialect = csv.excel

            reader = csv.reader(file, dialect)

            rows = list(reader)

            if not rows:
                return {
                    "valid": False,
                    "error": "The CSV contains no data.",
                }

            headers = rows[0]

            if not any(header.strip() for header in headers):
                return {
                    "valid": False,
                    "error": "The CSV does not contain valid headers.",
                }

            column_count = len(headers)

            malformed_rows = []

            for row_number, row in enumerate(rows[1:], start=2):

                if len(row) != column_count:
                    malformed_rows.append(row_number)

            return {
                "valid": len(malformed_rows) == 0,
                "delimiter": dialect.delimiter,
                "column_count": column_count,
                "row_count": len(rows) - 1,
                "headers": headers,
                "malformed_rows": malformed_rows,
                "error": (
                    "CSV contains malformed rows."
                    if malformed_rows
                    else None
                ),
            }

    except UnicodeDecodeError:
        return {
            "valid": False,
            "error": "The CSV encoding is not supported.",
        }

    except Exception as error:
        return {
            "valid": False,
            "error": f"Unable to validate CSV: {str(error)}",
        }
        
        
def parse_csv(file_path: str) -> dict:
    """
    Parse CSV data into structured records.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            sample = file.read(8192)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                dialect = csv.excel

            reader = csv.DictReader(
                file,
                dialect=dialect,
            )

            rows = list(reader)

            return {
                "headers": reader.fieldnames or [],
                "rows": rows,
                "row_count": len(rows),
            }

    except UnicodeDecodeError:
        raise ValueError(
            "The CSV encoding is not supported."
        )

    except Exception as error:
        raise ValueError(
            f"Unable to parse CSV: {str(error)}"
        )
        
        

def detect_csv_schema(rows: list[dict], headers: list[str]) -> list[dict]:
    """
    Detect basic schema information for CSV columns.
    """

    schema = []

    for column in headers:

        values = [
            row.get(column, "").strip()
            for row in rows
        ]

        non_empty_values = [
            value for value in values
            if value != ""
        ]

        missing_count = len(values) - len(non_empty_values)

        data_type = "string"

        if non_empty_values:

            if all(
                value.isdigit()
                for value in non_empty_values
            ):
                data_type = "integer"

            else:
                try:
                    for value in non_empty_values:
                        float(value)

                    data_type = "float"

                except ValueError:
                    data_type = "string"

        schema.append({
            "column": column,
            "data_type": data_type,
            "total_values": len(values),
            "missing_values": missing_count,
            "unique_values": len(set(non_empty_values)),
        })

    return schema


def profile_csv_data(
    rows: list[dict],
    schema: list[dict],
) -> list[dict]:
    """
    Generate basic profiling statistics for CSV columns.
    """

    profile = []

    for column_info in schema:

        column = column_info["column"]
        data_type = column_info["data_type"]

        values = [
            row.get(column, "").strip()
            for row in rows
        ]

        non_empty_values = [
            value for value in values
            if value != ""
        ]

        result = {
            "column": column,
            "data_type": data_type,
            "total_values": len(values),
            "missing_values": len(values) - len(non_empty_values),
            "unique_values": len(set(non_empty_values)),
        }

        if data_type in ("integer", "float") and non_empty_values:

            numeric_values = [
                float(value)
                for value in non_empty_values
            ]

            result.update({
                "min": min(numeric_values),
                "max": max(numeric_values),
                "average": round(
                    sum(numeric_values) / len(numeric_values),
                    2,
                ),
            })

        else:

            result.update({
                "min": None,
                "max": None,
                "average": None,
            })

        profile.append(result)

    return profile