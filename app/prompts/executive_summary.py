from app.schemas.result_analyzer import ResultAnalysis


def build_executive_summary_prompt(
    question: str,
    analysis: ResultAnalysis,
    query_result: list[dict]
) -> str:
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

Deterministic Numeric Statistics:
{analysis.numeric_summary}

Highest Value:
{analysis.highest_value}

Lowest Value:
{analysis.lowest_value}

These numeric statistics were calculated programmatically from the
query result. Treat them as authoritative. Do NOT recalculate or
contradict them.

When stating the highest or lowest result, use the provided
Highest Value and Lowest Value fields exactly.

Never infer or calculate a different highest or lowest value
from the query result.

Query Result:
{query_result}

Rules:

1. Answer based ONLY on the provided data.
2. Treat Deterministic Numeric Statistics as authoritative.
3. Never invent facts, numbers, trends, rankings, or explanations.
4. Directly address the user's question.
5. Keep the summary concise and business-oriented.
6. Mention important numerical findings when relevant.
7. When comparing numerical values, ensure the comparison is
   mathematically consistent with the provided statistics.
8. Never claim that a value is the highest when another provided value
   is larger.
9. Mention notable patterns or comparisons only when clearly supported.
10. If the result is empty, clearly state that no matching data was found.
11. Do not discuss SQL, databases, prompts, models, or implementation.
12. Return a structured response only.

The response must contain:

- summary: A concise overall explanation of the result.
- key_insights: A list of the most important findings.
"""

    return prompt.strip()