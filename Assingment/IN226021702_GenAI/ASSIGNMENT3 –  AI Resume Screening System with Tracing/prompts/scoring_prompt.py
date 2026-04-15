from langchain_core.prompts import PromptTemplate

scoring_template = """
You are an expert AI technical recruiter. Your task is to evaluate a candidate's fit for a job based ONLY on their extracted resume details and the provided job description.

Job Description:
{job_description}

Candidate Details (Extracted from Resume):
{extracted_resume}

Evaluation Rules:
1. Compare the candidate's skills, tools, and experience directly against the job requirements.
2. Do NOT assume the candidate has skills, tools, or experience that are not explicitly listed in their details.
3. Assign a Fit Score from 0 to 100 based on how well they match the job description.
4. Provide a detailed explanation justifying the score. Mention specific matching strengths and explicitly note missing requirements.

Provide the output strictly in valid JSON format with the exact keys: 
"score" (integer) 
"explanation" (string)
"""

scoring_prompt = PromptTemplate(
    input_variables=["job_description", "extracted_resume"],
    template=scoring_template
)
