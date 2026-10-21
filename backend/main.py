
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    return {
        "name": "OmniTutor AI",
        "status": "online",
        "message": "Welcome to OmniTutor AI"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
