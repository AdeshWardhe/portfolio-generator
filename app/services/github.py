import httpx
from os import getenv
from dotenv import load_dotenv

load_dotenv()

GITHUB_CLIENT_ID = getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = getenv("GITHUB_CLIENT_SECRET")
GITHUB_API_BASE = "https://api.github.com"

async def exchange_code_for_token(code: str) -> str:
    """Exchange the code GitHub sends us for an access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code
            }
        )
        data = response.json()
        return data.get("access_token")

async def fetch_github_user(access_token: str) -> dict:
    """Fetch the GitHub user's profile using their access token."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_BASE}/user", headers=headers)
        response.raise_for_status()
        return response.json()

async def fetch_github_repos(access_token: str) -> list:
    """Fetch all repos of the logged in user."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/user/repos",
            headers=headers,
            params={
                "sort": "updated",
                "per_page": 30,
                "type": "owner"
            }
        )
        response.raise_for_status()
        repos = response.json()
        # filter out forked repos
        return [r for r in repos if not r["fork"]]