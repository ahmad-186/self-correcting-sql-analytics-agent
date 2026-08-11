from app.graph.state import AgentState
from app.models.executive_summary import generate_executive_summary
from app.config.logging import get_logger

logger = get_logger(__name__)

def executive_summary_node(state: AgentState):

    question = state['question']
    analysis = state['result_analysis']
    query_result = state['query_result']

    logger.info("Executive summary generation started")

    summary = generate_executive_summary(
        question=question,
        analysis=analysis,
        query_result=query_result
    )

    logger.info("Executive summary generated successfully")


    return {"executive_summary": summary}