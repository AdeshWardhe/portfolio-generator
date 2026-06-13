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
  repoGrid.innerHTML = repos.map((repo, index) => `
    <div class="repo-card" data-index="${index}">
      <h3>${repo.name}</h3>
      <p class="repo-description" id="desc-${index}">${repo.description || "No description available"}</p>
      <div class="repo-meta">
        ${repo.language ? `<span class="repo-language">${repo.language}</span>` : ""}
        <span>⭐ ${repo.stars}</span>
        <span>🍴 ${repo.forks}</span>
      </div>
      <button class="btn-generate" onclick="handleGenerate(${index})">
        ✨ Generate AI Description
      </button>
    </div>
  `).join("");

  // store repos globally so handleGenerate can access them
  window.currentRepos = repos;
}

async function handleGenerate(index) {
  const repo = window.currentRepos[index];
  const descElement = document.getElementById(`desc-${index}`);
  const button = document.querySelector(`[data-index="${index}"] .btn-generate`);

  button.disabled = true;
  button.textContent = "Generating...";
  descElement.textContent = "🤖 AI is writing a description...";

  try {
    const newDescription = await generateDescription(token, repo);
    descElement.textContent = newDescription;
    button.textContent = "✅ Generated!";
  } catch (error) {
    console.error("Generation failed:", error);
    descElement.textContent = repo.description || "No description available";
    button.textContent = "✨ Generate AI Description";
    button.disabled = false;
  }
}

loadDashboard();