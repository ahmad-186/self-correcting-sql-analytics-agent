from typing import Any
from langchain_mistralai import ChatMistralAI
from app.config.settings import settings


llm = ChatMistralAI(
    model=settings.llm_model,
    api_key=settings.mistral_api_key,
    temperature=0
)

def get_llm() -> Any:
    """
    return the configured LLM instance.
    This implementation will be completed
    once an LLM provide is selected
    """

    return llm
