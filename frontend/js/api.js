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

// Calls FastAPI to generate an AI description for a repo
async function generateDescription(token, repo) {
  const response = await fetch(`${API_BASE}/generate/description`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      repo_name: repo.name,
      language: repo.language,
      topics: repo.topics,
      existing_description: repo.description
    })
  });

  if (!response.ok) {
    throw new Error("Failed to generate description");
  }

  const data = await response.json();
  return data.description;
}

// Saves the user's portfolio (title, tagline, selected projects)
async function savePortfolio(token, portfolioData) {
  const response = await fetch(`${API_BASE}/portfolio/save`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(portfolioData)
  });

  if (!response.ok) {
    throw new Error("Failed to save portfolio");
  }

  return await response.json();
}

// Publishes the portfolio (makes it publicly visible)
async function publishPortfolio(token) {
  const response = await fetch(`${API_BASE}/portfolio/publish`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error("Failed to publish portfolio");
  }

  return await response.json();
}