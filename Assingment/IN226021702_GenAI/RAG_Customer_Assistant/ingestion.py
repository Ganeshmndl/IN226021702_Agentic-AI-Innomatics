import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def run_ingestion():
    print("🚀 Starting optimized document ingestion...")

    # 1. Document Loader
    # Standard loader for the 27-page AlphaTech manual
    loader = PyPDFLoader("data/knowledge_base.pdf")
    raw_documents = loader.load()

    # 2. Optimized Chunking Strategy (LLD Requirement 2.0)
    # We increase chunk_size to 2000 to keep large specification tables intact.
    # We use custom separators to prioritize splitting at double newlines (paragraphs)
    # rather than in the middle of a table row.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""]
    )

    documents = text_splitter.split_documents(raw_documents)
    print(f"✅ Split into {len(documents)} high-context chunks.")

    # 3. Local Embedding Model (Technology Choice 5.0)
    # Using 'all-MiniLM-L6-v2' for efficient local processing
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Vector Store (Mandatory Concept #2)
    # Persisting to ./vectorstore for use in graph_engine.py
    print("📦 Saving to ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./vectorstore"
    )

    print("✨ Ingestion complete! Your optimized vector database is ready.")


if __name__ == "__main__":
    run_ingestion()
