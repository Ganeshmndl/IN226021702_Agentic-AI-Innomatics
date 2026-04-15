# 🚀 TalentTrace AI: Resume Screening Pipeline

An automated, hallucination-free AI pipeline that bridges the gap between candidate resumes and job descriptions using Large Language Models. Built for the Innomatics Technology Hub Data Science Internship.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-LCEL_Pipeline-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-F55036?style=for-the-badge)
![LangSmith](https://img.shields.io/badge/LangSmith-Observability-000000?style=for-the-badge)

---

## ⚙️ How It Works (The Pipeline)

This project leverages LangChain Expression Language (LCEL) to create a multi-stage evaluation process:

```text
📄 Resume Text ──> 🧠 Skill Extraction ──> ⚖️ JD Matching & Scoring ──> 📊 Explainable Output
                       (Strict JSON)           (Llama 3.3 70B)             (Score + Reasoning)
```
---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** LangChain (LangChain Expression Language)
- **LLM:** Meta Llama 3.3 (via Groq API)
- **Observability:** LangSmith

## 📁 Project Structure

```text
📦 ASSIGNMENT3
 ┣ 📂 chains/
 ┃ ┣ 📜 extraction_chain.py
 ┃ ┗ 📜 scoring_chain.py
 ┣ 📂 data/
 ┃ ┣ 📜 job_description.txt
 ┃ ┣ 📜 Emily_Chen.txt (Strong)
 ┃ ┣ 📜 Marcus_Johnson.txt (Average)
 ┃ ┣ 📜 Sophia_Patel.txt (Weak)
 ┃ ┗ 📜 David_Smith.txt (Unrelated)
 ┣ 📂 prompts/
 ┃ ┣ 📜 extraction_prompt.py
 ┃ ┗ 📜 scoring_prompt.py
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```
## 1️⃣ Set Up Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
---
## 2️⃣ Configure API Keys 🔐

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=Resume_Screening_Assignment
