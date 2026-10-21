# OmniTutor AI – Next-Gen Alexa+ Learning Companion

OmniTutor AI is a voice-driven agentic learning companion submitted to the **Amazon Developer Hackathon (Alexa+ Track & AWS Builder Mini Challenge)**. It emulates Alexa+ autonomous tool execution using the **Model Context Protocol (MCP)** and integrates **Amazon Bedrock** foundation models.

---

## 🚀 Key Features
- **Hands-Free Voice Interface:** Built with the browser Web Speech API for real-time speech recognition and synthesis.
- **Model Context Protocol (MCP) Tools:**
  - `generate_diagnostic_quiz`: Synthesizes dynamic conceptual multiple-choice checks.
  - `analyze_code_snippet`: Parses code logic and pinpoints boundary flaws.
  - `generate_study_milestones`: Automatically decomposes project deadlines into actionable daily plans.
- **Amazon Bedrock Reasoning:** Leverages AWS SDK `boto3` to evaluate user intent and synthesize natural voice responses.

---

## 🛠️ Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
