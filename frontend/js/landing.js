const connectBtn = document.getElementById("connectBtn");

connectBtn.addEventListener("click", async () => {
  connectBtn.disabled = true;
  connectBtn.textContent = "Redirecting...";

  try {
    const githubUrl = await getGithubLoginUrl();
    window.location.href = githubUrl;
  } catch (error) {
    console.error("Failed to get GitHub login URL:", error);
    connectBtn.disabled = false;
    connectBtn.textContent = "🐙 Connect GitHub";
  }
});