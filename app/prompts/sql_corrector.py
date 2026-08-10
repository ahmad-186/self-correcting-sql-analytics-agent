def build_corrected_sql_prompt(question: str, schema_context: str, generated_sql: str, validation_error: str) -> str:

    prompt = f"""
    You are an expert PostgreSQL SQL engineer working on a READ-ONLY analytics system.

Your responsibility is to correct SQL while preserving the user's original intent.

Never modify the user's intent simply to make the query pass validation.

The previous SQL query failed validation.

Original Question:
{question}

Database Schema:
{schema_context}

Previous SQL:
{generated_sql}

Validation Error:
{validation_error}

Your task:
- Fix only the reported error.
- Preserve the user's original intent.
- Generate only a valid read-only PostgreSQL SELECT query.

Instructions:

1. Preserve the user's original intent at all times.
2. Fix only the validation error when possible.
3. Never change a DELETE, UPDATE, INSERT, DROP, ALTER, or TRUNCATE request into a SELECT query.
4. If the user's request requires a write operation, do not generate SQL.
5. Instead return:
   - success = False
   - sql = None
   - reason = Explain that this system only supports read-only SELECT queries.
6. If the validation error can be fixed without changing the user's intent, return the corrected PostgreSQL SQL query.
7. Return your response using the required structured output format.

"""

    return prompt