from app.graph.state import AgentState
from app.tools.sql_executor import execute_sql

def sql_executor_node(state: AgentState):

    """
    Execute the validated SQL query.
    """

    generated_sql = state["generated_sql"]

    query_result  = execute_sql(generated_sql)

    return {"query_result": query_result }