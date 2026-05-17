from fastapi import APIRouter, HTTPException, Query
from data.loader import load_data
import pandas as pd

router = APIRouter()


def _genre_similarity(game_genres: str, target_genres: str) -> float:
    """Calculate Jaccard similarity between two genre strings."""
    g1 = set(str(game_genres).lower().split(";"))
    g2 = set(str(target_genres).lower().split(";"))
    if not g1 or not g2:
        return 0.0
    intersection = g1 & g2
    union = g1 | g2
    return len(intersection) / len(union)


@router.get("/by-genre")
def recommend_by_genre(
    genre: str = Query(..., description="Genre to filter by, e.g. 'Action', 'RPG'"),
    limit: int = Query(10, ge=1, le=50),
    min_approval: float = Query(0.7, ge=0.0, le=1.0, description="Minimum approval rate (0-1)")
):
    """Return top-rated games for a given genre."""
    df = load_data()

    if "genres" not in df.columns:
        raise HTTPException(status_code=500, detail="Dataset does not contain a 'genres' column.")

    mask = df["genres"].str.contains(genre, case=False, na=False)
    filtered = df[mask].copy()

    if "approval_rate" in filtered.columns:
        filtered = filtered[filtered["approval_rate"] >= min_approval]
        filtered = filtered.sort_values("approval_rate", ascending=False)

    if filtered.empty:
        raise HTTPException(status_code=404, detail=f"No games found for genre '{genre}'")

    return {
        "genre": genre,
        "min_approval": min_approval,
        "count": len(filtered.head(limit)),
        "results": filtered.head(limit).to_dict(orient="records")
    }


@router.get("/similar/{appid}")
def recommend_similar(
    appid: int,
    limit: int = Query(5, ge=1, le=20)
):
    """Return games similar to a given game based on genre similarity."""
    df = load_data()

    target = df[df["appid"] == appid]
    if target.empty:
        raise HTTPException(status_code=404, detail=f"Game with appid {appid} not found")

    target_genres = target.iloc[0].get("genres", "")
    others = df[df["appid"] != appid].copy()

    others["similarity"] = others["genres"].apply(
        lambda g: _genre_similarity(g, target_genres)
    )
    similar = others.sort_values("similarity", ascending=False).head(limit)

    return {
        "based_on": target.iloc[0].get("name", appid),
        "genres": target_genres,
        "results": similar[["appid", "name", "genres", "similarity"]].to_dict(orient="records")
    }
