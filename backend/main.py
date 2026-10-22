
import re
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env before importing the AI service.
load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bedrock_service import generate_answer
from mcp_tools import (
    generate_diagnostic_quiz,
    analyze_code_snippet,
    generate_study_milestones,
)

app = FastAPI(
    title="OmniTutor AI",
    description="Voice-powered AI tutoring assistant",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "name": "OmniTutor AI",
        "status": "online",
        "message": "Welcome to OmniTutor AI",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


def requested_days(message: str) -> int:
    """Read the requested number of days, defaulting to 3."""
    match = re.search(
        r"\b(\d{1,2})\s*[- ]?\s*days?\b",
        message.lower(),
    )

    if match:
        return max(1, min(int(match.group(1)), 30))

    word_numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    for word, number in word_numbers.items():
        if re.search(rf"\b{word}\s+days?\b", message.lower()):
            return number

    return 3


def looks_like_code(message: str) -> bool:
    """Recognize common Python code patterns."""
    patterns = [
        r"\bdef\s+\w+\s*\(",
        r"\bfor\s+\w+\s+in\s+",
        r"\bwhile\s+.+:",
        r"\bprint\s*\(",
        r"\bimport\s+\w+",
        r"\bif\s+.+:",
        r"\bclass\s+\w+",
        r"\brange\s*\(",
        r"\breturn\b",
        r"\btry\s*:",
    ]

    return any(
        re.search(pattern, message)
        for pattern in patterns
    )


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()
    lower = message.lower()

    if not message:
        return {
            "answer": "Please enter a question.",
            "tool": "none",
        }

    # 1. Study planner
    if any(
        phrase in lower
        for phrase in (
            "study plan",
            "study schedule",
            "learning plan",
            "milestone",
        )
    ):
        days = requested_days(message)
        result = generate_study_milestones(message, days=days)

    # 2. Practice quizzes
    elif any(
        phrase in lower
        for phrase in (
            "quiz",
            "test me",
            "practice test",
            "mock test",
            "exam questions",
        )
    ):
        result = generate_diagnostic_quiz(message)

    # 3. Code debugging and explanations
    elif (
        any(
            phrase in lower
            for phrase in (
                "debug",
                "debugging",
                "review this code",
                "analyze this code",
                "analyse this code",
                "find the bug",
                "explain this code",
                "explain this python code",
                "what does this code do",
                "fix this code",
                "correct this code",
                "check this code",
            )
        )
        or (
            looks_like_code(message)
            and any(
                phrase in lower
                for phrase in (
                    "explain",
                    "error",
                    "bug",
                    "fix",
                    "output",
                    "correct",
                    "why",
                )
            )
        )
    ):
        result = analyze_code_snippet(message)

    # 4. General questions use the configured Gemini service.
    else:
        answer = generate_answer(message)

        return {
            "answer": answer,
            "tool": "gemini_conversation",
        }

    return {
        "answer": (
            result.get("message")
            or f"I used the {result['tool']} tutoring tool."
        ),
        "tool": result["tool"],
        "result": result,
    }
