from fastapi import FastAPI

app = FastAPI(
    title="Developer Productivity Platform",
    description="Codebase intelligence platform for understanding and navigating software projects.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Developer Productivity Platform API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}