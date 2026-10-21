
import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def get_bedrock_client():
    """Create a Bedrock Runtime client using standard AWS credentials."""
    region = os.getenv("AWS_REGION", "us-east-1")

    return boto3.client(
        "bedrock-runtime",
        region_name=region,
    )


def generate_answer(prompt: str) -> str:
    """Generate a response using an Amazon Bedrock model."""
    model_id = os.getenv(
        "BEDROCK_MODEL_ID",
        "anthropic.claude-3-haiku-20240307-v1:0",
    )

    try:
        client = get_bedrock_client()

        response = client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
            inferenceConfig={
                "maxTokens": 600,
                "temperature": 0.5,
            },
        )

        return response["output"]["message"]["content"][0]["text"]

    except (BotoCoreError, ClientError) as exc:
        print(f"Bedrock request failed: {type(exc).__name__}")
        return (
            "Amazon Bedrock is not available right now. "
            "Please check your AWS credentials, region, model access, "
            "and permissions."
        )
