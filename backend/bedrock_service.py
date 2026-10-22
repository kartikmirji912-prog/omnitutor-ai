
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load the API key from backend/.env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-3.5-flash-lite"


def generate_answer(prompt: str) -> str:
    """Generate an answer using Google Gemini."""

    if not GEMINI_API_KEY:
        print(
            "ERROR: GEMINI_API_KEY is missing from backend/.env",
            file=sys.stderr,
            flush=True,
        )
        return "Gemini API key is missing. Check backend/.env."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            answer = (response.text or "").strip()

            if answer:
                return answer

            print(
                "Gemini returned an empty response.",
                file=sys.stderr,
                flush=True,
            )
            return "Gemini returned an empty response. Please try again."

        finally:
            client.close()

    except errors.APIError as exc:
        # Do not print or expose the API key.
        print(
            f"Gemini API error (HTTP {getattr(exc, 'code', 'unknown')}): {exc}",
            file=sys.stderr,
            flush=True,
        )
        return (
            "Gemini API request failed. Check the backend terminal "
            "for the error details."
        )

    except Exception as exc:
        print(
            f"Unexpected Gemini error: {type(exc).__name__}: {exc}",
            file=sys.stderr,
            flush=True,
        )
        return "Could not connect to Gemini. Check the backend terminal."
