from app.graph.state import AgentState
from app.tools.schema_inspector import inspect_schema

def schema_inspector_node(state: AgentState):
    """
    Retrieve the relevant database schema and update the graph state
    """

    question = state["question"]

    schema = inspect_schema(question)

    return { "schema_context": schema["schema_context"], "database_schema": schema["database_schema"]}