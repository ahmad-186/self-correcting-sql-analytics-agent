from app.schemas.result_analyzer import ResultAnalysis

def build_executive_summary_prompt(question: str, analysis: ResultAnalysis, query_result: list[dict]) -> str:

    """
    Build the prompt for the Executive Summary LLM.
    """

    prompt = f"""
You are an expert business data analyst.

Your task is to analyze the SQL query result and provide a concise,
accurate executive summary for a business user.

User Question:
{question}

Result Analysis:
- Row Count: {analysis.row_count}
- Columns: {analysis.column_names}
- Numeric Columns: {analysis.numeric_columns}
- Categorical Columns: {analysis.categorical_columns}
- Datetime Columns: {analysis.datetime_columns}
- Is Empty: {analysis.is_empty}

Query Result:
{query_result}

Rules:

1. Answer based ONLY on the provided query result.
2. Do not invent facts, numbers, trends, or explanations.
3. Directly address the user's question.
4. Keep the summary concise and business-oriented.
5. Mention important numerical findings when relevant.
6. Mention notable patterns or comparisons when they are clearly
   supported by the data.
7. If the result is empty, clearly state that no matching data was found.
8. Do not discuss SQL or implementation details.
9. Return a structured response only.

The response must contain:
- summary: A concise overall explanation of the result.
- key_insights: A list of the most important findings.
"""

    return prompt.strip()