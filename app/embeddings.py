from langchain_mistralai import MistralAIEmbeddings
from app.config.settings import settings

embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=settings.mistral_api_key
)