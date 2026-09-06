from app.services.llm_service import generate_answer


def build_insight_prompt(
    document_text: str,
    file_type: str,
) -> str:
    """
    Build a prompt to extract important information
    from a PDF or CSV document.
    """

    if not document_text.strip():
        raise ValueError(
            "Document text cannot be empty."
        )

    return f"""
You are StarQ's document analysis engine.

Analyze the provided {file_type.upper()} content
and extract the most important information.

Return ONLY valid JSON in this format:

{{
    "title": "short document title",
    "summary": "2-3 sentence summary",
    "key_points": [
        "important point 1",
        "important point 2",
        "important point 3"
    ],
    "entities": [
        "important person, company, place or organization"
    ],
    "topics": [
        "main topic 1",
        "main topic 2"
    ]
}}

Rules:
1. Use ONLY the provided document content.
2. Do not invent information.
3. Keep key points concise.
4. Include only information supported by the document.
5. Return valid JSON only.

DOCUMENT CONTENT:
--------------------
{document_text}
--------------------
""".strip()


def extract_important_information(
    document_text: str,
    file_type: str,
) -> str:
    """
    Extract important information using the LLM.
    """

    prompt = build_insight_prompt(
        document_text=document_text,
        file_type=file_type,
    )

    return generate_answer(prompt)


def build_key_insights(
    statistics: dict,
    important_information: dict | None = None,
) -> list[str]:
    """
    Generate human-readable key insights from
    document statistics and extracted information.
    """

    insights = []

    if not statistics:
        return insights

    # PDF insights
    if "page_count" in statistics:

        page_count = statistics["page_count"]
        text_pages = statistics.get(
            "text_pages",
            0,
        )
        empty_pages = statistics.get(
            "empty_pages",
            0,
        )
        total_images = statistics.get(
            "total_images",
            0,
        )
        total_words = statistics.get(
            "total_words",
            0,
        )

        insights.append(
            f"The document contains {page_count} pages."
        )

        if text_pages:
            insights.append(
                f"{text_pages} pages contain extractable text."
            )

        if empty_pages:
            insights.append(
                f"{empty_pages} pages contain no extractable text."
            )

        if total_images:
            insights.append(
                f"The document contains approximately "
                f"{total_images} embedded images."
            )

        if total_words:
            insights.append(
                f"The document contains approximately "
                f"{total_words:,} words."
            )

    # CSV insights
    if "row_count" in statistics:

        row_count = statistics["row_count"]
        column_count = statistics.get(
            "column_count",
            0,
        )
        missing_values = statistics.get(
            "missing_values",
            0,
        )

        insights.append(
            f"The dataset contains {row_count:,} rows "
            f"and {column_count} columns."
        )

        if missing_values:
            insights.append(
                f"The dataset contains "
                f"{missing_values:,} missing values."
            )
        else:
            insights.append(
                "The dataset contains no missing values."
            )

    # Important information
    if important_information:

        topics = important_information.get(
            "topics",
            [],
        )

        if topics:
            insights.append(
                "Main topics: "
                + ", ".join(topics[:5])
                + "."
            )

    return insights