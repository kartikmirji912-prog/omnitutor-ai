
from mcp.server.fastmcp import FastMCP

from mcp_tools import (
    generate_diagnostic_quiz,
    analyze_code_snippet,
    generate_study_milestones,
)

mcp = FastMCP("OmniTutor AI")


@mcp.tool()
def learn_topic(topic: str) -> str:
    """Create a simple explanation of a learning topic."""
    from bedrock_service import generate_answer

    return str(
        generate_answer(
            f"Teach me {topic} in simple words with an example."
        )
    )


@mcp.tool()
def generate_quiz(topic: str) -> dict:
    """Generate a practice quiz about a subject."""
    return generate_diagnostic_quiz(topic)


@mcp.tool()
def analyze_code(code: str) -> dict:
    """Analyze Python code and provide suggestions."""
    # Pass the actual code without adding extra text.
    return analyze_code_snippet(code, language="Python")


@mcp.tool()
def create_study_plan(topic: str, days: int = 5) -> dict:
    """Create a study plan for a topic and number of days."""
    days = max(1, min(int(days), 30))

    return generate_study_milestones(
        topic,
        days=days,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
