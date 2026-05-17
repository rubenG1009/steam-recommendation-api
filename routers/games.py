from fastapi import APIRouter, HTTPException, Query
from data.loader import load_data

router = APIRouter()


@router.get("/")
def get_all_games(
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """Return a paginated list of all games."""
    df = load_data()
    total = len(df)
    page = df.iloc[offset:offset + limit]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": page.to_dict(orient="records")
    }


@router.get("/search")
def search_games(
    q: str = Query(..., description="Search term (game name)"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search games by name."""
    df = load_data()
    mask = df["name"].str.contains(q, case=False, na=False)
    results = df[mask].head(limit)
    if results.empty:
        raise HTTPException(status_code=404, detail=f"No games found matching '{q}'")
    return {"query": q, "count": len(results), "results": results.to_dict(orient="records")}


@router.get("/{appid}")
def get_game_by_id(appid: int):
    """Return a single game by its Steam AppID."""
    df = load_data()
    game = df[df["appid"] == appid]
    if game.empty:
        raise HTTPException(status_code=404, detail=f"Game with appid {appid} not found")
    return game.iloc[0].to_dict()
