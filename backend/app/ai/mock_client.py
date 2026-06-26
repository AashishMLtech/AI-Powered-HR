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
        base_jd = jd.strip()
        platform_templates = {
            "linkedin": (
                f"Now hiring: {job_title}\n\n"
                "We are looking for a thoughtful professional who brings ownership, clear communication, "
                "and a strong sense of collaboration.\n\n"
                "What you will do:\n"
                f"{base_jd}\n\n"
                "Why this role stands out:\n"
                "- Work on meaningful problems with visible business impact.\n"
                "- Join a team that values learning, accountability, and steady growth.\n"
                "- Share ideas, improve processes, and help shape how the team works.\n\n"
                "Best fit for:\n"
                "Candidates who want a stable, growth-focused environment and enjoy building with purpose."
            ),
            "twitter": (
                f"{job_title} opportunity\n\n"
                f"{base_jd}\n\n"
                "Looking for candidates who move fast, communicate clearly, and like solving real problems.\n"
                "Apply now."
            ),
            "facebook": (
                f"We’re hiring: {job_title}\n\n"
                f"{base_jd}\n\n"
                "This is a great fit for candidates looking for a supportive team, practical work, and room to grow.\n"
                "Please share with anyone who may be interested."
            ),
            "instagram": (
                f"Now hiring: {job_title}\n\n"
                f"{base_jd}\n\n"
                "Ideal for creative, motivated candidates who want to learn, contribute, and grow with a team."
            ),
        }
        return platform_templates.get(platform, platform_templates["linkedin"])

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
