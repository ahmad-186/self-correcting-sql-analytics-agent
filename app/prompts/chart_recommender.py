from app.schemas.result_analyzer import ResultAnalysis


def build_chart_prompt(
    question: str,
    analysis: ResultAnalysis,
) -> str:
    """
    Build the prompt for the chart recommendation LLM.
    """

    prompt = f"""
You are an expert data visualization assistant.

Your job is to recommend the BEST visualization for the user's request.

Available chart types:

- BAR
- LINE
- PIE
- SCATTER
- TABLE
- NONE

User Question:
{question}

Query Result Analysis

Row Count:
{analysis.row_count}

Columns:
{analysis.column_names}

Numeric Columns:
{analysis.numeric_columns}

Categorical Columns:
{analysis.categorical_columns}

Datetime Columns:
{analysis.datetime_columns}

Is Empty:
{analysis.is_empty}

Rules:

1. Recommend ONLY ONE chart type.

2. Choose the best x_axis.

3. Choose the best y_axis.

4. Generate a short professional chart title.

5. Explain your reasoning briefly.

6. If the data should not be visualized,
   return chart_type=TABLE.

7. Only use the provided column names.

8. Never invent columns.

9. Return a structured response only.

IMPORTANT:
The chart_type value MUST be exactly one of:
"bar", "line", "pie", "scatter", "table", "none"

Use lowercase values exactly as written.
Do NOT return enum names such as BAR, LINE, TABLE, or NONE.

"""

    return prompt.strip()