import re


def extract_github_username(github_url: str) -> str:
    match = re.search(r"github\.com/([^/\s]+)", github_url or "")
    return match.group(1) if match else ""


async def get_public_github_summary(github_url: str) -> dict:
    username = extract_github_username(github_url)
    if not username:
        return {"username": "", "repo_count": 0, "languages": []}

    # Kept offline-friendly for fresher local setup. A real version would call GitHub REST API.
    return {
        "username": username,
        "repo_count": 3,
        "languages": ["Python", "TypeScript", "SQL"],
    }
