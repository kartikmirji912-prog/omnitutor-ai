
import ast
import re
from typing import Any


def clean_topic(text: str) -> str:
    return text.strip() or "General study"


def extract_code(code: str) -> str:
    code = code.strip()
    code = re.sub(r"^```(?:python)?\s*", "", code)
    code = re.sub(r"\s*```$", "", code)
    return code.strip()


def explain_python_code(tree: ast.AST, code: str) -> str:
    if any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree)):
        return "This code contains a loop that repeats instructions."
    if any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)):
        return "This code defines a function that can be called."
    if any(isinstance(node, ast.If) for node in ast.walk(tree)):
        return "This code uses a condition to choose which instructions to run."
    return "This is valid Python syntax. Review the code to understand its exact behaviour."


def generate_diagnostic_quiz(
    topic: str, difficulty: str = "intermediate"
) -> dict[str, Any]:
    lower = topic.lower()

    if "loop" in lower or "for loop" in lower or "while" in lower:
        questions = [
            {
                "question": "What does range(3) produce?",
                "options": ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "Only 3"],
                "answer": "0, 1, 2",
            },
            {
                "question": "Which loop is commonly used to iterate over a list?",
                "options": ["for", "if", "def", "import"],
                "answer": "for",
            },
            {
                "question": "How many times does for i in range(5) run?",
                "options": ["4", "5", "6", "1"],
                "answer": "5",
            },
            {
                "question": "Which keyword exits a loop immediately?",
                "options": ["stop", "exit", "break", "skip"],
                "answer": "break",
            },
            {
                "question": "Which keyword skips to the next loop iteration?",
                "options": ["continue", "pass", "break", "next"],
                "answer": "continue",
            },
        ]
    elif "python" in lower:
        questions = [
            {
                "question": "Which symbol starts a comment in Python?",
                "options": ["#", "//", "/*", "--"],
                "answer": "#",
            },
            {
                "question": "Which function displays output?",
                "options": ["show()", "print()", "output()", "write()"],
                "answer": "print()",
            },
            {
                "question": "What is the result of 2 + 3?",
                "options": ["23", "5", "6", "Error"],
                "answer": "5",
            },
        ]
    else:
        questions = [
            {
                "question": f"What is a good first step when learning {topic}?",
                "options": [
                    "Understand the basics",
                    "Skip all concepts",
                    "Avoid practice",
                    "Memorize without understanding",
                ],
                "answer": "Understand the basics",
            },
            {
                "question": f"How can you improve your understanding of {topic}?",
                "options": [
                    "Practise examples",
                    "Never revise",
                    "Ignore mistakes",
                    "Avoid questions",
                ],
                "answer": "Practise examples",
            },
        ]

    return {
        "tool": "generate_diagnostic_quiz",
        "topic": topic,
        "difficulty": difficulty,
        "questions": questions,
    }


def analyze_code_snippet(
    code: str, language: str = "Python"
) -> dict[str, Any]:
    cleaned_code = extract_code(code)
    issues: list[dict[str, str]] = []
    suggestions: list[str] = []

    if not cleaned_code:
        return {
            "tool": "analyze_code_snippet",
            "language": language,
            "code": "",
            "issues_found": [
                {
                    "severity": "High",
                    "description": "No code was provided.",
                }
            ],
            "suggestions": ["Enter code and try again."],
            "explanation": "There is no code to explain yet.",
            "corrected_code": None,
            "message": "Please provide code to analyze.",
        }

    if language.strip().lower() not in ("python", "py"):
        return {
            "tool": "analyze_code_snippet",
            "language": language,
            "code": cleaned_code,
            "issues_found": [],
            "suggestions": ["Detailed analysis currently supports Python only."],
            "explanation": "Please submit Python code.",
            "corrected_code": None,
            "message": "This language is not yet supported.",
        }

    try:
        tree = ast.parse(cleaned_code)
        explanation = explain_python_code(tree, cleaned_code)
    except SyntaxError as error:
        issues.append(
            {
                "severity": "High",
                "description": f"Syntax error on line {error.lineno}: {error.msg}",
            }
        )
        explanation = "Python could not parse the code. Check the reported line."

    if not issues:
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Div)
                and isinstance(node.right, ast.Constant)
                and node.right.value == 0
            ):
                issues.append(
                    {
                        "severity": "High",
                        "description": "Division by zero will cause an error.",
                    }
                )
                suggestions.append("Check the denominator before dividing.")
                break

    if not issues:
        suggestions.append("No obvious issue found in these basic checks.")

    return {
        "tool": "analyze_code_snippet",
        "language": language,
        "code": cleaned_code,
        "issues_found": issues,
        "suggestions": suggestions,
        "explanation": explanation,
        "corrected_code": None,
        "message": "Potential issues found." if issues else "Basic checks passed.",
    }


def generate_study_milestones(
    topic: str, days: int = 3
) -> dict[str, Any]:
    clean = clean_topic(topic)
    days = max(1, min(int(days), 30))

    plan = [
        ("Learn the basics", f"Study the fundamentals of {clean}."),
        ("Study examples", f"Follow examples related to {clean}."),
        ("Practise", f"Solve practice questions about {clean}."),
        ("Review", f"Revise difficult concepts in {clean}."),
        ("Apply your knowledge", f"Complete a small task using {clean}."),
        ("Test yourself", f"Answer questions about {clean}."),
        ("Final revision", f"Review your notes on {clean}."),
    ]

    milestones = []
    for day in range(1, days + 1):
        focus, task = plan[(day - 1) % len(plan)]
        milestones.append({"day": day, "focus": focus, "task": task})

    return {
        "tool": "generate_study_milestones",
        "topic": clean,
        "timeline_days": days,
        "milestones": milestones,
    }
