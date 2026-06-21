from app.ai.base_client import BaseLLMClient
from app.ai.gemini_client import GeminiClient
from app.ai.groq_client import GroqClient
from app.ai.mock_client import MockLLMClient
from app.config import get_settings


def get_llm_client() -> BaseLLMClient:
    settings = get_settings()

    if settings.gemini_api_key:
        fallback = GroqClient(settings.groq_api_key) if settings.groq_api_key else MockLLMClient()
        return GeminiClient(settings.gemini_api_key, fallback=fallback)

    if settings.groq_api_key:
        return GroqClient(settings.groq_api_key)

    return MockLLMClient()
