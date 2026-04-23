import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langgraph.graph import StateGraph, END
# Simplified Memory [cite: 582]
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# 1. Improved State Object (Matches LLD 2.3) [cite: 538]


class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    category: str
    # Memory support for multi-turn conversations [cite: 582]
    history: List[str]


# 2. Setup: Increased 'k' to fetch full tables
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./vectorstore",
                     embedding_function=embeddings)

# SUGGESTION: Increased k from 3 to 6 to capture full table context [cite: 576]
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 3. Nodes (Graph Execution Module) [cite: 532]


def retrieve_node(state: AgentState):
    print("---LOG: Retrieval Module Active---")
    docs = retriever.invoke(state["question"])
    if not docs:  # Error Handling [cite: 554]
        return {"context": "No relevant technical documentation found."}

    # Metadata tracking helps with "Data Flow" explanation in HLD [cite: 511-512]
    content = "\n".join(
        [f"Source: {d.metadata.get('source')} - {d.page_content}" for d in docs])
    return {"context": content}


def categorize_node(state: AgentState):
    print("---LOG: Intent Detection Module Active---")
    q = state["question"].lower()
    # HITL Escalation Criteria (LLD 4.0) [cite: 543, 546]
    critical_keywords = ["ransomware",
                         "security breach", "data exfiltration", "hacked"]
    if any(word in q for word in critical_keywords):
        return {"category": "CRITICAL"}
    return {"category": "GENERAL"}


def generate_node(state: AgentState):
    print("---LOG: Query Processing Module Active---")

    # We join the history into a string so the LLM can read it
    chat_history = "\n".join(state.get("history", []))

    prompt = f"""You are an AlphaTech Support Assistant.
    Below is the conversation history and the technical context.
    
    CONVERSATION HISTORY:
    {chat_history}
    
    TECHNICAL CONTEXT:
    {state['context']}
    
    CURRENT QUESTION: 
    {state['question']}
    
    Answer concisely. If the user refers to 'it' or 'previous', use the history to find the subject."""

    response = llm.invoke(prompt)

    # CRITICAL: We return the new answer AND append it to the history
    new_history = state.get("history", [])
    new_history.append(f"User: {state['question']}")
    new_history.append(f"Assistant: {response.content}")

    return {"answer": response.content, "history": new_history}


def human_escalation_node(state: AgentState):
    # HITL Module [cite: 533, 547]
    print("---LOG: HITL Escalation Triggered---")
    return {"answer": "🚨 CRITICAL: This query matches a Security HITL Trigger. A SOC Analyst has been notified for manual review."}


# 4. Workflow Design (LangGraph) [cite: 539-540]
workflow = StateGraph(AgentState)

# Add Processing Nodes
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("categorize", categorize_node)
workflow.add_node("generate", generate_node)
workflow.add_node("escalate", human_escalation_node)

# Define Logic Flow (Edges)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "categorize")

# Conditional Routing Logic [cite: 542, 572]


def route_logic(state: AgentState):
    if state["category"] == "CRITICAL":
        return "escalate"
    return "generate"


workflow.add_conditional_edges(
    "categorize",
    route_logic,
    {"escalate": "escalate", "generate": "generate"}
)

workflow.add_edge("generate", END)
workflow.add_edge("escalate", END)

# 5. Persistence Module Integration [cite: 533, 582]
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
