from fastapi import FastAPI

app = FastAPI(
    title="Portfolio Generator API",
    description="AI-powered developer portfolio generator",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Portfolio Generator API is running"}