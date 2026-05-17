from fastapi import APIRouter, HTTPException, Query
from data.loader import load_data

router = APIRouter()


@router.get("/overview")
def dataset_overview():
    """General stats about the dataset."""
    df = load_data()
    stats = {
        "total_games": len(df),
        "columns": list(df.columns),
    }
    if "price" in df.columns:
        stats["avg_price"] = round(df["price"].mean(), 2)
        stats["free_games"] = int((df["price"] == 0).sum())
    if "approval_rate" in df.columns:
        stats["avg_approval_rate"] = round(df["approval_rate"].mean(), 2)
    return stats


@router.get("/top-rated")
def top_rated(
    limit: int = Query(10, ge=1, le=50),
    min_ratings: int = Query(1000, description="Minimum number of ratings to qualify")
):
    """Return the highest-rated games with a minimum number of ratings."""
    df = load_data()

    if "approval_rate" not in df.columns:
        raise HTTPException(status_code=500, detail="approval_rate column not available.")

    filtered = df.copy()
    if "positive_ratings" in df.columns:
        total = df["positive_ratings"] + df.get("negative_ratings", 0)
        filtered = df[total >= min_ratings]

    top = filtered.sort_values("approval_rate", ascending=False).head(limit)
    return {
        "min_ratings_threshold": min_ratings,
        "count": len(top),
        "results": top.to_dict(orient="records")
    }


@router.get("/by-developer")
def games_by_developer(
    developer: str = Query(..., description="Developer name to search"),
    limit: int = Query(20, ge=1, le=100)
):
    """Return all games from a specific developer."""
    df = load_data()
    if "developer" not in df.columns:
        raise HTTPException(status_code=500, detail="developer column not available.")
    mask = df["developer"].str.contains(developer, case=False, na=False)
    results = df[mask].head(limit)
    if results.empty:
        raise HTTPException(status_code=404, detail=f"No games found for developer '{developer}'")
    return {"developer": developer, "count": len(results), "results": results.to_dict(orient="records")}
