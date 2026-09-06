from app.services.insight_service import (
    build_key_insights,
)


def test_pdf_insights():

    statistics = {
        "page_count": 102,
        "text_pages": 98,
        "empty_pages": 4,
        "total_words": 25000,
        "total_characters": 150000,
        "total_images": 35,
    }

    insights = build_key_insights(
        statistics
    )

    assert len(insights) > 0

    assert any(
        "102 pages" in insight
        for insight in insights
    )

    assert any(
        "98 pages" in insight
        for insight in insights
    )

    assert any(
        "35 embedded images" in insight
        for insight in insights
    )

    assert any(
        "25,000 words" in insight
        for insight in insights
    )

    print("PDF key insights: PASSED")

    for insight in insights:
        print("-", insight)


def test_csv_insights():

    statistics = {
        "row_count": 1250,
        "column_count": 12,
        "missing_values": 37,
    }

    insights = build_key_insights(
        statistics
    )

    assert len(insights) > 0

    assert any(
        "1,250 rows" in insight
        for insight in insights
    )

    assert any(
        "12 columns" in insight
        for insight in insights
    )

    assert any(
        "37 missing values" in insight
        for insight in insights
    )

    print("CSV key insights: PASSED")


def test_empty_statistics():

    insights = build_key_insights({})

    assert insights == []

    print("Empty statistics handling: PASSED")


if __name__ == "__main__":

    test_pdf_insights()
    test_csv_insights()
    test_empty_statistics()

    print("\n6.5 Key Insights Test: PASSED")