const API_BASE = "http://localhost:8000";

// Calls FastAPI to get the GitHub login URL
async function getGithubLoginUrl() {
  const response = await fetch(`${API_BASE}/auth/github/login`);
  const data = await response.json();
  return data.url;
}


// Calls FastAPI to get the user's GitHub repos (requires JWT token)
async function getRepos(token) {
  const response = await fetch(`${API_BASE}/repos/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error("Failed to fetch repos");
  }

  return await response.json();
}