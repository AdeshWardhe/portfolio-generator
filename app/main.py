from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth, repos

app = FastAPI(
    title="Portfolio Generator API",
    description="AI-powered developer portfolio generator",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(repos.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Portfolio Generator API is running"}

# Serve frontend files — must be LAST so API routes are checked first
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")