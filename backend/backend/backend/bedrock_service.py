"""
AWS Bedrock Integration for OmniTutor AI (Alexa+ Simulator).
Uses boto3 to communicate with Amazon Bedrock foundation models.
"""
import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from mcp_tools import execute_mcp_tool

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

def get_bedrock_client():
    try:
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=AWS_REGION
        )
    except Exception as e:
        print(f"[Bedrock] Warning: Could not initialize boto3 client: {e}")
        return None

def process_alexa_turn(user_prompt: str):
    client = get_bedrock_client()
    lowered = user_prompt.lower()

    chosen_tool = None
    tool_args = {}

    if any(k in lowered for k in ["quiz", "test", "question", "exam", "practice"]):
        chosen_tool = "generate_diagnostic_quiz"
        tool_args = {"topic": user_prompt.replace("quiz", "").strip() or "Computer Science Foundations", "question_count": 2}
    elif any(k in lowered for k in ["code", "bug", "syntax", "error", "python", "function"]):
        chosen_tool = "analyze_code_snippet"
        tool_args = {"language": "Python", "code": user_prompt, "goal": "Debug and optimize logic"}
    elif any(k in lowered for k in ["plan", "schedule", "milestone", "days", "prepare", "study"]):
        chosen_tool = "generate_study_milestones"
        tool_args = {"goal": user_prompt, "days_available": 3}

    tool_output = None
    if chosen_tool:
        tool_output = execute_mcp_tool(chosen_tool, tool_args)

    spoken_summary = ""
    if client:
        try:
            prompt_payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [
                    {
                        "role": "user",
                        "content": f"You are Alexa+ running OmniTutor. A user requested: '{user_prompt}'. "
                                   f"Tool executed: {chosen_tool}. Output: {json.dumps(tool_output)}. "
                                   f"Provide a natural, encouraging voice response in 2-3 sentences."
                    }
                ]
            }
            response = client.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps(prompt_payload),
                contentType="application/json",
                accept="application/json"
            )
            response_body = json.loads(response["body"].read())
            spoken_summary = response_body["content"][0]["text"]
        except (BotoCoreError, ClientError, Exception) as err:
            print(f"[Bedrock runtime info]: {err}")

    if not spoken_summary:
        if chosen_tool == "generate_diagnostic_quiz":
            spoken_summary = f"I've generated a diagnostic quiz on {tool_args.get('topic', 'your topic')} using my MCP quiz tool. Let's tackle these questions together!"
        elif chosen_tool == "analyze_code_snippet":
            spoken_summary = "I've analyzed your code snippet. I found a couple of key areas to optimize memory and fix index boundaries."
        elif chosen_tool == "generate_study_milestones":
            spoken_summary = "I've structured a milestone study schedule for your timeline. Check out the three-phase breakdown on your screen."
        else:
            spoken_summary = "I'm OmniTutor on Alexa+. I can build dynamic quizzes, debug code snippets, or lay out a custom study plan. What shall we tackle?"

    return {
        "alexa_voice_response": spoken_summary,
        "tool_used": chosen_tool,
        "tool_data": tool_output,
        "provider": "Amazon Bedrock (Runtime API)" if client else "Alexa+ Simulated MCP Engine (AWS Bedrock Ready)"
    }
