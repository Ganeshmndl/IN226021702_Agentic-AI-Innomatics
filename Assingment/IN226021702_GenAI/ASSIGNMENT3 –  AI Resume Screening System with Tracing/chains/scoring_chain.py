from prompts.scoring_prompt import scoring_prompt
from langchain_core.output_parsers import JsonOutputParser


def get_scoring_chain(llm):
    """
    Creates an LCEL chain for scoring a candidate's extracted details against a job description.
    """
    parser = JsonOutputParser()

    # LCEL pipeline: Prompt -> LLM -> JSON Parser
    chain = scoring_prompt | llm | parser

    return chain
