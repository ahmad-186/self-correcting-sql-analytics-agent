from app.models.client import llm
from app.schemas.executive_summary import ExecutiveSummary
from app.prompts.executive_summary import build_executive_summary_prompt

structured_llm = llm.with_structured_output(ExecutiveSummary)

def generate_executive_summary(question: str, analysis, query_result: list[dict]) -> ExecutiveSummary:
    """
    Generate an executive summary from the query result.
    """

    prompt = build_executive_summary_prompt(
        question=question,
        analysis=analysis,
        query_result=query_result
    )

    response = structured_llm.invoke(prompt)

    return response