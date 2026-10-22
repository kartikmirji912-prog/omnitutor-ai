# OmniTutor AI — Your AI Learning Companion

OmniTutor AI is an AI-powered learning companion built for the **Amazon Developer Hackathon**, targeting the **Alexa+ Track** and AWS Builder Mini Challenge. It combines learning tools, voice interaction, and the **Model Context Protocol (MCP)** to demonstrate how an AI assistant can use tools to help students learn.

## 🚀 Key Features

- **Voice Interaction:** Uses browser speech recognition and text-to-speech where supported.
- **Learn a Topic:** Get simple explanations and examples.
- **Practice Quiz:** Generate questions to test your understanding.
- **Code Assistant:** Analyze code and identify potential issues.
- **Study Planner:** Break a learning goal into a daily study plan.
- **MCP Tool Server:** Exposes learning capabilities through four tools.

## 🧰 MCP Tools

The MCP server is implemented in `backend/mcp_server.py`.

| Tool | Purpose |
|---|---|
| `learn_topic` | Explains a topic in simple words with an example. |
| `generate_quiz` | Creates a practice quiz about a subject. |
| `analyze_code` | Checks code and provides suggestions. |
| `create_study_plan` | Creates a study plan for a topic and number of days. |

## 🛠️ Local Setup

### Requirements

- Python 3.10 or newer
- Git
- A modern browser

### 1. Start the backend

Open PowerShell in the project folder and run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

The API documentation should be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Start the frontend

Open a **second terminal** in the project folder and run:

```powershell
cd frontend
python -m http.server 5500
```

Then open [http://127.0.0.1:5500](http://127.0.0.1:5500) in your browser.

### 3. Test the MCP tools

Open another terminal in the `backend` folder, activate the virtual environment, and run:

```powershell
python test_mcp.py
```

The MCP server uses standard input/output (stdio) transport. An MCP-compatible client is needed to connect to it directly.

## ☁️ Amazon Bedrock

The project includes a Bedrock integration. Successful model calls depend on valid AWS credentials, model access, region configuration, and account permissions. If Bedrock is unavailable, the application may use its local fallback behavior.

**Never commit API keys, credentials, or `.env` files to GitHub.**

## 🏗️ Technology Stack

- Python and FastAPI
- Model Context Protocol (MCP)
- Amazon Bedrock integration
- HTML, CSS, and JavaScript
- Browser Web Speech API

## 🎯 Hackathon Goal

OmniTutor AI demonstrates an MCP-powered learning assistant that can select and run focused tools for quizzes, code analysis, topic explanations, and study planning. It is a simulated Alexa+ style experience rather than an official Alexa+ integration.

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE).
