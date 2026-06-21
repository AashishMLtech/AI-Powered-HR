from app.ai.base_client import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    async def rewrite_jd(self, raw_text: str, title: str) -> str:
        return (
            f"# {title}\n\n"
            "We are hiring for a motivated professional who can take ownership, communicate clearly, "
            "and deliver reliable work in a collaborative team.\n\n"
            "## Role Overview\n"
            f"{raw_text.strip()}\n\n"
            "## Responsibilities\n"
            "- Understand business requirements and turn them into practical work.\n"
            "- Collaborate with HR, hiring managers, and team members.\n"
            "- Keep documentation clear and communicate progress regularly.\n\n"
            "## Requirements\n"
            "- Strong fundamentals and willingness to learn.\n"
            "- Good problem-solving and communication skills.\n"
            "- Ability to work responsibly with feedback.\n\n"
            "## Benefits\n"
            "A supportive environment, learning opportunities, and meaningful projects."
        )

    async def social_caption(self, platform: str, job_title: str, jd: str) -> str:
        captions = {
            "linkedin": f"We are hiring a {job_title}. Join a team that values ownership, clarity, and growth.",
            "twitter": f"We are hiring: {job_title}. Apply now and grow with a collaborative team.",
            "facebook": f"New opening for {job_title}. Share this with someone ready for their next role.",
            "instagram": f"Now hiring: {job_title}. Build, learn, and grow with us.",
        }
        return captions.get(platform, captions["linkedin"])

    async def score_cv(self, resume_text: str, job_title: str, jd: str) -> dict:
        score = 65
        lowered = resume_text.lower()
        for word in ["python", "react", "sql", "fastapi", "next.js", "typescript"]:
            if word in lowered:
                score += 5
        return {
            "score": min(score, 95),
            "reasoning": "Resume has relevant keywords and appears broadly aligned with the role.",
        }

    async def assess_github(self, github_summary: dict, job_title: str) -> dict:
        if not github_summary.get("username"):
            return {"score": 0, "reasoning": "No GitHub profile was provided."}
        repo_count = github_summary.get("repo_count", 0)
        score = min(80, 35 + repo_count * 10)
        return {"score": score, "reasoning": "Public GitHub activity shows basic technical consistency."}

    async def ai_resume_flag(self, resume_text: str) -> dict:
        repeated = resume_text.lower().count("passionate") + resume_text.lower().count("dynamic")
        flag = min(80, repeated * 20)
        return {
            "score": flag,
            "reasoning": "Advisory heuristic only. A higher value means the resume may need closer human review.",
        }
