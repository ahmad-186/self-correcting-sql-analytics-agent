from app.graph.state import AgentState
from app.schemas.response import AnalyticsResponse

def response_formatter_node(state: AgentState):

    response = AnalyticsResponse(
        question=state['question'],
        summary=state['executive_summary'],
        chart=state['chart_config'],
        result=state['query_result']
    )

    return {
        "final_response": response
    }