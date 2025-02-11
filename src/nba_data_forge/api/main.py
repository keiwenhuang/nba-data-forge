from fastapi import FastAPI

from nba_data_forge.api.v1 import router

app = FastAPI(
    title="NBA Data Forge",
    version="1.0.0",
    description="API for accessing NBA game statistics and analytics",
)


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
