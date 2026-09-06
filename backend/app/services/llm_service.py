import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def generate_answer(prompt: str) -> str:
    """
    Generate a grounded answer using Gemini.

    The model is configured for low-latency responses
    because StarQ is a document question-answering system.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        generation_config={
            "thinking_level": "low",
        },
    )

    if not interaction.output_text:
        raise RuntimeError(
            "LLM returned an empty response."
        )

    return interaction.output_text.strip()