
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
    version="1.0.0",
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


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()
    lower = message.lower()

    if any(word in lower for word in ["quiz", "test", "exam"]):
        result = generate_diagnostic_quiz(message)
    elif any(word in lower for word in ["debug", "code", "bug", "error"]):
        result = analyze_code_snippet(message)
    elif any(word in lower for word in ["study plan", "schedule", "milestone"]):
        result = generate_study_milestones(message)
    else:
        return {
            "answer": generate_answer(message),
            "tool": "bedrock_conversation",
        }

    return {
        "answer": f"I used the {result['tool']} tutoring tool.",
        "tool": result["tool"],
        "result": result,
    }
