from app.graph.state import AgentState
from app.models.chart_recommender import recommended_chart
from app.schemas.chart_config import ChartConfig

def visualization_node(state: AgentState):

    analysis = state["result_analysis"]
    question = state["question"]
    query_result = state["query_result"]

    recommendation = recommended_chart(question=question, analysis=analysis)

    chart_config =  ChartConfig(
        chart_type=recommendation.chart_type,
        title=recommendation.title,
        x_axis=recommendation.x_axis,
        y_axis=recommendation.y_axis,
        data = query_result
    )

    return {"chart_config": chart_config}