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
      <label class="checkbox-label">
        <input type="checkbox" class="repo-checkbox" data-index="${index}">
        Include in portfolio
      </label>
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

// Handle "Save Portfolio" button click
document.getElementById("saveBtn").addEventListener("click", async () => {
  const title = document.getElementById("portfolioTitle").value || "My Portfolio";
  const tagline = document.getElementById("portfolioTagline").value;

  // gather selected repos
  const checkboxes = document.querySelectorAll(".repo-checkbox:checked");
  const selectedProjects = [];

  checkboxes.forEach((checkbox, order) => {
    const index = checkbox.dataset.index;
    const repo = window.currentRepos[index];
    const descElement = document.getElementById(`desc-${index}`);

    selectedProjects.push({
      repo_name: repo.name,
      repo_url: repo.url,
      language: repo.language,
      ai_description: descElement.textContent,
      display_order: order
    });
  });

  if (selectedProjects.length === 0) {
    alert("Please select at least one repo to include in your portfolio!");
    return;
  }

  const saveBtn = document.getElementById("saveBtn");
  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    await savePortfolio(token, { title, tagline, projects: selectedProjects });
    saveBtn.textContent = "✅ Saved!";
  } catch (error) {
    console.error("Save failed:", error);
    saveBtn.textContent = "❌ Failed - Try Again";
  }

  setTimeout(() => {
    saveBtn.disabled = false;
    saveBtn.textContent = "💾 Save Portfolio";
  }, 2000);
});

// Handle "Publish Portfolio" button click
document.getElementById("publishBtn").addEventListener("click", async () => {
  const publishBtn = document.getElementById("publishBtn");
  const messageEl = document.getElementById("publishMessage");

  publishBtn.disabled = true;
  publishBtn.textContent = "Publishing...";

  try {
    const result = await publishPortfolio(token);
    const fullUrl = `${window.location.origin}${result.public_url}`;
    messageEl.innerHTML = `🎉 Your portfolio is live! <a href="${result.public_url}" target="_blank">${fullUrl}</a>`;
    publishBtn.textContent = "🌐 Publish Portfolio";
  } catch (error) {
    console.error("Publish failed:", error);
    messageEl.textContent = "❌ Failed to publish. Save your portfolio first!";
    publishBtn.textContent = "🌐 Publish Portfolio";
  }

  publishBtn.disabled = false;
});