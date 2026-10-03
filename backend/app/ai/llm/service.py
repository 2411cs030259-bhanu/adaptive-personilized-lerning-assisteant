from app.core.config import settings
from .demo import DemoLLM
from .groq import GroqLLM
def provider():
    if settings.llm_provider.lower()=="groq" and settings.llm_api_key:
        return GroqLLM(settings.llm_api_key,settings.llm_model)
    return DemoLLM()
