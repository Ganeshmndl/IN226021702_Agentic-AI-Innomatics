import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Import custom chains
from chains.extraction_chain import get_extraction_chain
from chains.scoring_chain import get_scoring_chain

load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize chains
extraction_chain = get_extraction_chain(llm)
scoring_chain = get_scoring_chain(llm)

# File paths
jd_path = "data/job_description.txt"
resume_files = [
    "data/Emily_Chen.txt",
    "data/Marcus_Johnson.txt",
    "data/Sophia_Patel.txt",
    "data/David_Smith.txt"
]

# Load Job Description
with open(jd_path, "r", encoding="utf-8") as f:
    jd_content = f.read()

print("🚀 Starting AI Resume Screening Pipeline...\n")
print("=" * 50)

# Loop through each resume and process it
for resume_path in resume_files:
    candidate_name = resume_path.split(
        "/")[-1].replace(".txt", "").replace("_", " ")
    print(f"📄 Evaluating Candidate: {candidate_name}")

    try:
        # Load Resume
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_content = f.read()

        # Step 1: Extract Skills
        print("   -> Extracting details...")
        extracted_data = extraction_chain.invoke(
            {"resume_text": resume_content})

        # Step 2: Score Candidate
        print("   -> Scoring candidate against Job Description...")
        scoring_result = scoring_chain.invoke({
            "job_description": jd_content,
            "extracted_resume": extracted_data
        })

        # Output Results
        print(f"\n✅ Result for {candidate_name}:")
        print(f"   ⭐ Score: {scoring_result.get('score')}/100")
        print(f"   💡 Explanation: {scoring_result.get('explanation')}\n")

    except Exception as e:
        print(f"❌ Error processing {candidate_name}: {e}\n")

    print("-" * 50)

print("\n🎉 Pipeline Complete! Check LangSmith for your 4 trace runs.")
