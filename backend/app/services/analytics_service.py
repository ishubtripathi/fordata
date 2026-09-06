def build_visual_analytics(
    statistics: dict,
) -> dict:
    """
    Convert document statistics into
    dashboard-ready chart data.
    """

    if not statistics:
        return {}

    analytics = {}

    # PDF analytics
    if "page_count" in statistics:

        analytics["page_distribution"] = {
            "labels": [
                "Text Pages",
                "Empty Pages",
            ],
            "values": [
                statistics.get("text_pages", 0),
                statistics.get("empty_pages", 0),
            ],
        }

        analytics["content_metrics"] = {
            "labels": [
                "Words",
                "Characters",
                "Images",
            ],
            "values": [
                statistics.get("total_words", 0),
                statistics.get("total_characters", 0),
                statistics.get("total_images", 0),
            ],
        }

    # CSV analytics
    if "row_count" in statistics:

        total_cells = (
            statistics.get("row_count", 0)
            * statistics.get("column_count", 0)
        )

        missing_values = statistics.get(
            "missing_values",
            0,
        )

        available_values = max(
            total_cells - missing_values,
            0,
        )

        analytics["data_quality"] = {
            "labels": [
                "Available Values",
                "Missing Values",
            ],
            "values": [
                available_values,
                missing_values,
            ],
        }

        analytics["dataset_size"] = {
            "labels": [
                "Rows",
                "Columns",
            ],
            "values": [
                statistics.get("row_count", 0),
                statistics.get("column_count", 0),
            ],
        }

    return analytics