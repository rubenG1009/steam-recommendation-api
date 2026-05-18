from fastapi import FastAPI, HTTPException, Query
from loader import load_data

app = FastAPI(
    title="Steam Game Recommendation API",
    description="""
RESTful API that serves Steam game data and recommendations.
Built with FastAPI and Pandas. Full ETL pipeline available in the repo.

**Endpoints:**
- `/games` — Browse and search games
- `/recommend` — Get recommendations by genre or similar games
- `/stats` — Dataset statistics and top-rated games

**GitHub:** https://github.com/rubenG1009/steam-recommendation-api
""",
    version="1.0.0",
    contact={
        "name": "Rubén García Revett",
        "url": "https://linkedin.com/in/ruben-garcia-revett-b72312223",
    }
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Steam Game Recommendation API",
        "version": "1.0.0",
        "total_games": len(load_data()),
        "docs": "/docs",
        "endpoints": ["/games", "/games/search", "/games/{appid}",
                      "/recommend/by-genre", "/recommend/similar/{appid}",
                      "/stats/overview", "/stats/top-rated", "/stats/by-developer"]
    }


# ── GAMES ─────────────────────────────────────────────────────────────────────

@app.get("/games", tags=["Games"])
def get_games(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Paginated list of all games."""
    df = load_data()
    page = df.iloc[offset:offset + limit]
    return {"total": len(df), "limit": limit, "offset": offset,
            "results": page.to_dict(orient="records")}


@app.get("/games/search", tags=["Games"])
def search_games(
    q: str = Query(..., description="Search term"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search games by name."""
    df = load_data()
    results = df[df["name"].str.contains(q, case=False, na=False)].head(limit)
    if results.empty:
        raise HTTPException(404, detail=f"No games found matching '{q}'")
    return {"query": q, "count": len(results), "results": results.to_dict(orient="records")}


@app.get("/games/{appid}", tags=["Games"])
def get_game(appid: int):
    """Get a game by Steam AppID."""
    df = load_data()
    game = df[df["appid"] == appid]
    if game.empty:
        raise HTTPException(404, detail=f"Game with appid {appid} not found")
    return game.iloc[0].to_dict()


# ── RECOMMEND ─────────────────────────────────────────────────────────────────

@app.get("/recommend/by-genre", tags=["Recommendations"])
def recommend_by_genre(
    genre: str = Query(..., description="Genre e.g. Action, RPG, Strategy"),
    limit: int = Query(5, ge=1, le=20),
    min_approval: float = Query(0.7, ge=0.0, le=1.0)
):
    """Top-rated games for a given genre."""
    df = load_data()
    filtered = df[df["genres"].str.contains(genre, case=False, na=False)].copy()
    filtered = filtered[filtered["approval_rate"] >= min_approval]
    filtered = filtered.sort_values("approval_rate", ascending=False).head(limit)
    if filtered.empty:
        raise HTTPException(404, detail=f"No games found for genre '{genre}' with approval >= {min_approval}")
    return {"genre": genre, "min_approval": min_approval,
            "count": len(filtered), "results": filtered.to_dict(orient="records")}


@app.get("/recommend/similar/{appid}", tags=["Recommendations"])
def recommend_similar(appid: int, limit: int = Query(5, ge=1, le=10)):
    """Games similar to a given game based on genre similarity."""
    df = load_data()
    target = df[df["appid"] == appid]
    if target.empty:
        raise HTTPException(404, detail=f"Game {appid} not found")
    target_genres = set(str(target.iloc[0]["genres"]).lower().split(";"))
    others = df[df["appid"] != appid].copy()

    def similarity(g):
        g2 = set(str(g).lower().split(";"))
        if not g2:
            return 0.0
        return len(target_genres & g2) / len(target_genres | g2)

    others["similarity"] = others["genres"].apply(similarity)
    similar = others.sort_values("similarity", ascending=False).head(limit)
    return {
        "based_on": target.iloc[0]["name"],
        "genres": target.iloc[0]["genres"],
        "results": similar[["appid", "name", "genres", "similarity", "approval_rate"]].to_dict(orient="records")
    }


# ── STATS ─────────────────────────────────────────────────────────────────────

@app.get("/stats/overview", tags=["Stats"])
def overview():
    """General dataset statistics."""
    df = load_data()
    return {
        "total_games": len(df),
        "free_games": int((df["price"] == 0).sum()),
        "avg_price": round(df["price"].mean(), 2),
        "avg_approval_rate": round(df["approval_rate"].mean(), 3),
        "genres_available": sorted(set(
            g.strip() for genres in df["genres"].dropna()
            for g in genres.split(";")
        )),
        "developers": df["developer"].nunique()
    }


@app.get("/stats/top-rated", tags=["Stats"])
def top_rated(limit: int = Query(10, ge=1, le=25)):
    """Highest approval rate games."""
    df = load_data()
    top = df.sort_values("approval_rate", ascending=False).head(limit)
    return {"count": len(top), "results": top.to_dict(orient="records")}


@app.get("/stats/by-developer", tags=["Stats"])
def by_developer(developer: str = Query(..., description="Developer name")):
    """All games from a specific developer."""
    df = load_data()
    results = df[df["developer"].str.contains(developer, case=False, na=False)]
    if results.empty:
        raise HTTPException(404, detail=f"No games found for developer '{developer}'")
    return {"developer": developer, "count": len(results),
            "results": results.to_dict(orient="records")}
