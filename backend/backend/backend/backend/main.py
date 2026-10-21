from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bedrock_service import process_alexa_turn
from mcp_tools import MCP_TOOL_DEFINITIONS

app = FastAPI(title="OmniTutor AI - Alexa+ MCP Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {
        "service": "OmniTutor AI",
        "track": "Alexa+ MCP Simulation",
        "aws_services": ["Amazon Bedrock", "AWS SDK boto3"],
        "status": "healthy"
    }

@app.get("/api/mcp/tools")
def list_mcp_tools():
    return {"tools": MCP_TOOL_DEFINITIONS}

@app.post("/api/alexa/interact")
def interact_with_alexa(req: PromptRequest):
    return process_alexa_turn(req.message)
