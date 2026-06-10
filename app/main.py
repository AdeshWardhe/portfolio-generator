from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, repos

app = FastAPI(
    title="Portfolio Generator API",
    description="AI-powered developer portfolio generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(repos.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Portfolio Generator API is running"}