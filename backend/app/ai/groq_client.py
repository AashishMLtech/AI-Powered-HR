from app.ai.base_client import BaseLLMClient
from app.ai.mock_client import MockLLMClient


class GroqClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.mock = MockLLMClient()

    async def rewrite_jd(self, raw_text: str, title: str) -> str:
        return await self.mock.rewrite_jd(raw_text, title)

    async def social_caption(self, platform: str, job_title: str, jd: str) -> str:
        return await self.mock.social_caption(platform, job_title, jd)

    async def score_cv(self, resume_text: str, job_title: str, jd: str) -> dict:
        return await self.mock.score_cv(resume_text, job_title, jd)

    async def assess_github(self, github_summary: dict, job_title: str) -> dict:
        return await self.mock.assess_github(github_summary, job_title)

    async def ai_resume_flag(self, resume_text: str) -> dict:
        return await self.mock.ai_resume_flag(resume_text)
