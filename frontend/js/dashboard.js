// Step 1: Get token from URL or localStorage
const urlParams = new URLSearchParams(window.location.search);
const tokenFromUrl = urlParams.get("token");

if (tokenFromUrl) {
  // save it and clean up the URL
  localStorage.setItem("token", tokenFromUrl);
  window.history.replaceState({}, document.title, "/dashboard.html");
}

const token = localStorage.getItem("token");

// Step 2: If no token at all, send user back to landing page
if (!token) {
  window.location.href = "/";
}

// Step 3: Fetch and display repos
async function loadDashboard() {
  try {
    const data = await getRepos(token);
    renderProfile(data.profile);
    renderRepos(data.repos);
  } catch (error) {
    console.error("Failed to load dashboard:", error);
    localStorage.removeItem("token");
    window.location.href = "/";
  }
}

function renderProfile(profile) {
  const profileHeader = document.getElementById("profileHeader");
  profileHeader.innerHTML = `
    <img src="${profile.avatar_url}" alt="${profile.username}">
    <div class="profile-info">
      <h2>${profile.name || profile.username}</h2>
      <p>${profile.bio || "No bio available"}</p>
      <div class="profile-stats">
        <span>👥 ${profile.followers} followers</span>
        <span>📦 ${profile.public_repos} repos</span>
      </div>
    </div>
  `;
}

function renderRepos(repos) {
  const repoGrid = document.getElementById("repoGrid");
  repoGrid.innerHTML = repos.map(repo => `
    <div class="repo-card">
      <h3>${repo.name}</h3>
      <p>${repo.description || "No description available"}</p>
      <div class="repo-meta">
        ${repo.language ? `<span class="repo-language">${repo.language}</span>` : ""}
        <span>⭐ ${repo.stars}</span>
        <span>🍴 ${repo.forks}</span>
      </div>
    </div>
  `).join("");
}

loadDashboard();