from app.graph.state import AgentState
from app.models.executive_summary import generate_executive_summary

def executive_summary_node(state: AgentState):

    question = state['question']
    analysis = state['result_analysis']
    query_result = state['query_result']

    summary = generate_executive_summary(
        question=question,
        analysis=analysis,
        query_result=query_result
    )

    return {"executive_summary": summary}