from typing import Any


def build_document_overview(
    filename: str,
    file_type: str,
    file_size: int,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build a standardized overview for an uploaded document.
    """

    overview = {
        "filename": filename,
        "file_type": file_type,
        "file_size_bytes": file_size,
    }

    if metadata:
        overview["metadata"] = metadata

    return overview