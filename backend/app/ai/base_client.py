from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def rewrite_jd(self, raw_text: str, title: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def social_caption(self, platform: str, job_title: str, jd: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def score_cv(self, resume_text: str, job_title: str, jd: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def assess_github(self, github_summary: dict, job_title: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def ai_resume_flag(self, resume_text: str) -> dict:
        raise NotImplementedError
