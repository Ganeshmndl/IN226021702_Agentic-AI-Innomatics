from langchain_core.prompts import PromptTemplate

extraction_template = """
You are an expert technical AI recruiter. Your task is to extract specific information from the provided resume.
Do NOT assume skills not present in the resume. Extract ONLY what is explicitly stated.

Extract the following information:
1. Skills (List of technical and soft skills)
2. Experience (Total years of experience, or a brief summary if exact years aren't clear)
3. Tools (Software, frameworks, or platforms mentioned)

Resume Text:
{resume_text}

Provide the output strictly in valid JSON format with the exact keys: "skills", "experience", and "tools".
"""

# Define the PromptTemplate
extraction_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=extraction_template
)
