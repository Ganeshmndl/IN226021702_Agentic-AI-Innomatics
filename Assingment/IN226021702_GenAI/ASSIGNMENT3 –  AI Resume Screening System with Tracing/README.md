# 🚀 GenAI - AI Resume Screening System with Tracing

An internship-grade AI application for recruiter-style resume evaluation against a Job Description.

## 🚀 Snapshot

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-darkgreen?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLM_Provider-black?style=flat-square)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-purple?style=flat-square)
![Submission](https://img.shields.io/badge/Submission-Internship_Ready-brightgreen?style=flat-square)

## ✨ Key Features

- 📄 **Automated Resume Extraction**
- 📋 **Job Description Matching** against target role requirements
- 🧠 **Modular AI Pipeline (LCEL)**:
  - Step 1: Candidate profile extraction (Strict JSON parsing)
  - Step 2: Final recruiter decision and scoring logic
- 📊 **Fit Score + Gap Analysis**: Provides a 0-100 score with detailed explanations of matching strengths and missing skills
- 🔍 **Zero Hallucination Constraints**: Strict prompt engineering ensures the model does not assume skills not present in the resume
- 👁️ **Pipeline Transparency**: Full integration with LangSmith for real-time monitoring, debugging, and tracing

---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** LangChain (LangChain Expression Language)
- **LLM:** Meta Llama 3.3 (via Groq API)
- **Observability:** LangSmith

## 📁 Project Structure

```text
├── chains/
│   ├── extraction_chain.py
│   └── scoring_chain.py
├── data/
│   ├── job_description.txt
│   ├── Emily_Chen.txt
│   ├── Marcus_Johnson.txt
│   ├── Sophia_Patel.txt
│   └── David_Smith.txt
├── prompts/
│   ├── extraction_prompt.py
│   └── scoring_prompt.py
├── main.py
├── README.md
└── requirements.txt
```
