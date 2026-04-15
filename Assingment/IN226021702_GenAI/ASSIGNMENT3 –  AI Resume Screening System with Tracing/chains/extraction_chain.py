from prompts.extraction_prompt import extraction_prompt
from langchain_core.output_parsers import JsonOutputParser


def get_extraction_chain(llm):
    """
    Creates an LCEL chain for extracting skills, experience, and tools from a resume.
    """
    # The JsonOutputParser ensures the LLM's text output is converted into a Python dictionary
    parser = JsonOutputParser()

    # LCEL pipeline: Prompt -> LLM -> JSON Parser
    chain = extraction_prompt | llm | parser

    return chain
