import httpx
from os import getenv
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_project_description(repo_name: str, language: str, topics: list, existing_description: str) -> str:
    """
    Sends repo info to Groq's AI and gets back a polished project description.
    """
    prompt = f"""Write a professional, recruiter-friendly description (2-3 sentences) for a developer portfolio project with these details:

Project name: {repo_name}
Programming language: {language or "Not specified"}
Topics/tags: {", ".join(topics) if topics else "None"}
Current description: {existing_description or "None provided"}

Write only the description text, no extra commentary, no quotes around it."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"].strip()