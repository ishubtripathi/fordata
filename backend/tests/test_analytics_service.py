from app.services.analytics_service import (
    build_visual_analytics,
)


def test_pdf_analytics():

    statistics = {
        "page_count": 100,
        "text_pages": 95,
        "empty_pages": 5,
        "total_words": 20000,
        "total_characters": 120000,
        "total_images": 30,
    }

    analytics = build_visual_analytics(
        statistics
    )

    assert "page_distribution" in analytics
    assert "content_metrics" in analytics

    assert analytics["page_distribution"]["values"] == [
        95,
        5,
    ]

    assert analytics["content_metrics"]["values"] == [
        20000,
        120000,
        30,
    ]

    print("PDF visual analytics: PASSED")


def test_csv_analytics():

    statistics = {
        "row_count": 1000,
        "column_count": 10,
        "missing_values": 25,
    }

    analytics = build_visual_analytics(
        statistics
    )

    assert "data_quality" in analytics
    assert "dataset_size" in analytics

    assert analytics["data_quality"]["values"] == [
        9975,
        25,
    ]

    assert analytics["dataset_size"]["values"] == [
        1000,
        10,
    ]

    print("CSV visual analytics: PASSED")


def test_empty_statistics():

    analytics = build_visual_analytics({})

    assert analytics == {}

    print("Empty analytics handling: PASSED")


if __name__ == "__main__":

    test_pdf_analytics()
    test_csv_analytics()
    test_empty_statistics()

    print("\n6.6 Visual Analytics Test: PASSED")