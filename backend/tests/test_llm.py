from app.services.llm_service import generate_answer


def test_llm():

    prompt = (
        "Answer in one short sentence. "
        "What is a PDF?"
    )

    answer = generate_answer(prompt)

    assert isinstance(answer, str)
    assert len(answer) > 0

    print("LLM response:")
    print(answer)

    print("\n5.3 LLM Integration Test: PASSED")


if __name__ == "__main__":
    test_llm()