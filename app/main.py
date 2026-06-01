from fastapi import FastAPI
from src.app.routes import chat

app = FastAPI(
    title="Email Support with HITL",
    description="API for email support agent with human-in-the-loop feature",
    version="0.1.0",
)


app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Email Support API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )