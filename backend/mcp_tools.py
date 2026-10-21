
def generate_diagnostic_quiz(topic: str, difficulty: str = "intermediate"):
    """Generate a basic diagnostic quiz for a study topic."""
    return {
        "tool": "generate_diagnostic_quiz",
        "topic": topic,
        "difficulty": difficulty,
        "questions": [
            {
                "question": f"What is one important concept in {topic}?",
                "options": [
                    "A fundamental concept",
                    "An unrelated concept",
                    "None of the above"
                ],
                "answer": "A fundamental concept"
            },
            {
                "question": f"Why should you practise {topic}?",
                "options": [
                    "To improve understanding",
                    "To avoid learning",
                    "To skip revision"
                ],
                "answer": "To improve understanding"
            }
        ]
    }


def analyze_code_snippet(code: str, language: str = "Python"):
    """Return the submitted code for analysis by the tutoring service."""
    issues = []

    if "range(len(" in code and "[i+1]" in code.replace(" ", ""):
        issues.append({
            "severity": "High",
            "description": (
                "Check for an out-of-range access when using i + 1 "
                "on the final loop iteration."
            )
        })

    return {
        "tool": "analyze_code_snippet",
        "language": language,
        "code": code,
        "issues_found": issues,
        "message": (
            "Potential issues identified. Review the code and its "
            "boundary conditions."
        )
    }


def generate_study_milestones(topic: str, days: int = 3):
    """Create a simple study schedule."""
    days = max(1, min(days, 30))

    milestones = []
    for day in range(1, days + 1):
        milestones.append({
            "day": day,
            "focus": f"{topic}: study and practice",
            "task": (
                "Review key concepts, solve practice questions, "
                "and revise mistakes."
            )
        })

    return {
        "tool": "generate_study_milestones",
        "topic": topic,
        "timeline_days": days,
        "milestones": milestones
    }
