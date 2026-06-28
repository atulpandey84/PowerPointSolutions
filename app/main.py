from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Architecture Review Copilot (ARC)",
    description="Enterprise-grade agentic AI platform for architecture analysis and correction.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
