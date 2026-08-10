from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.graph.nodes.schema_inspector import schema_inspector_node
from app.graph.nodes.sql_generator import sql_generator_node
from app.graph.nodes.sql_validator import sql_validator_node
from app.graph.nodes.sql_executor import sql_executor_node
from app.graph.nodes.sql_corrector import sql_corrector_node
from app.graph.nodes.sql_result_analyzer import result_analyzer_node
from app.graph.nodes.visualization import visualization_node
from app.graph.nodes.executive_summary import executive_summary_node
from app.graph.nodes.response_formatter import response_formatter_node

from app.graph.routers.sql_validator_router import route_after_validation

# Define Graph
builder = StateGraph(AgentState)

# Nodes
builder.add_node("schema_inspector", schema_inspector_node)
builder.add_node("sql_generator", sql_generator_node)
builder.add_node("sql_validator", sql_validator_node)
builder.add_node("sql_executor", sql_executor_node)
builder.add_node("sql_corrector", sql_corrector_node)
builder.add_node("result_analyzer", result_analyzer_node)
builder.add_node("visualizer", visualization_node)
builder.add_node('executive_summary', executive_summary_node)
builder.add_node("response_formatter", response_formatter_node)

# Edges
# Linear Flow
builder.add_edge(START, "schema_inspector")
builder.add_edge("schema_inspector", "sql_generator")
builder.add_edge("sql_generator", "sql_validator")

# Conditional Routing
builder.add_conditional_edges(
    "sql_validator",
    route_after_validation,
    {
        "sql_executor": "sql_executor",
        "sql_corrector": "sql_corrector",
        END:END
    }
)

# Retry Loop
builder.add_edge("sql_corrector", "sql_validator")

# Finish
builder.add_edge("sql_executor", "result_analyzer")
builder.add_edge("result_analyzer", "visualizer")
builder.add_edge("result_analyzer", "executive_summary")

builder.add_edge("visualizer", "response_formatter")
builder.add_edge("executive_summary", "response_formatter")
builder.add_edge("response_formatter", END)


# Compile
graph = builder.compile()