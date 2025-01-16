from fastapi import FastAPI

app = FastAPI(
    title="NBA Data Forge",
    version="1.0.0",
    description="API for accessing NBA game statistics and analytics",
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
