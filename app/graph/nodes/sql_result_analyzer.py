from app.graph.state import AgentState
from app.tools.result_analyzer import analyze_result

def result_analyzer_node(state: AgentState):

    question = state["question"]
    query_result = state["query_result"]

    analysis = analyze_result(query_result)

    return {
        "result_analysis": analysis
    }