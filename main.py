from fastapi import FastAPI
from routers import games, recommendations, stats

app = FastAPI(
    title="Steam Game Recommendation API",
    description="RESTful API that serves game data and recommendations from a Steam dataset processed via ETL pipeline.",
    version="1.0.0"
)

app.include_router(games.router, prefix="/games", tags=["Games"])
app.include_router(recommendations.router, prefix="/recommend", tags=["Recommendations"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])

@app.get("/")
def root():
    return {
        "message": "Steam Recommendation API",
        "version": "1.0.0",
        "docs": "/docs"
    }
