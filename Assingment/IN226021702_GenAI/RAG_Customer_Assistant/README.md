# 🚀 AlphaTech Intelligent Support Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade **Agentic RAG (Retrieval-Augmented Generation)** system designed to automate technical support for AlphaTech Solutions. This agent utilizes a state-machine architecture to provide accurate technical answers from product manuals while implementing safety guardrails for security escalations.

---

## 📽️ Project Demo

> **Note:** Insert your LinkedIn presentation video link here!

---

## 🧠 Key Features

- **Stateful Memory:** Powered by LangGraph's `MemorySaver`, allowing the agent to remember conversation history and resolve contextual queries (e.g., _"What about its GPU?"_).
- **Intelligent Routing:** Automatically distinguishes between general technical queries and critical security threats using intent classification.
- **Human-in-the-Loop (HITL):** Implements a dedicated escalation node that bypasses AI generation for high-risk scenarios (Ransomware, Data Breaches).
- **High-Performance RAG:** Optimized ingestion pipeline with a 2000-character chunking strategy to preserve complex technical tables.
- **Local Embeddings:** Uses `all-MiniLM-L6-v2` for zero-latency, cost-effective vector search.

---

## 🛠️ Tech Stack

| Component           | Technology                      |
| :------------------ | :------------------------------ |
| **LLM**             | Meta Llama 3.3 (via Groq Cloud) |
| **Orchestration**   | LangGraph                       |
| **Vector Database** | ChromaDB                        |
| **Embeddings**      | HuggingFace (Local)             |
| **Framework**       | LangChain                       |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/AlphaTech-Support-Agent.git](https://github.com/YOUR_USERNAME/AlphaTech-Support-Agent.git)
cd AlphaTech-Support-Agent
```

---

## ⚙️ Setup Instructions

### 1. Set Up Environment

Create a `.env` file in the root directory:
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here

---

### 2. Install Dependencies

````bash
pip install -r requirements.txt

---
### 4. Run Ingestion

Process the 27-page technical manual into the vector database:

```bash
python ingestion.py

---
### 5. Launch the Agent

Start the interactive CLI support session:

```bash
python main.py
---

````
