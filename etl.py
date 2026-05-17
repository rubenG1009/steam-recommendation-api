"""
ETL Pipeline — Steam Dataset
Extracts, transforms and loads raw Steam data into a clean CSV ready for the API.
"""

import pandas as pd
import os

RAW_PATH = "data/steam_raw.csv"
CLEAN_PATH = "data/steam_clean.csv"


def extract(path: str) -> pd.DataFrame:
    print(f"[ETL] Extracting data from {path}...")
    df = pd.read_csv(path)
    print(f"[ETL] Loaded {len(df)} raw records.")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    print("[ETL] Transforming data...")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop duplicates
    df = df.drop_duplicates(subset=["appid"] if "appid" in df.columns else None)

    # Keep only relevant columns if they exist
    keep_cols = ["appid", "name", "genres", "tags", "positive_ratings",
                 "negative_ratings", "price", "release_date", "developer"]
    existing = [c for c in keep_cols if c in df.columns]
    df = df[existing]

    # Fill missing values
    df["genres"] = df["genres"].fillna("Unknown")
    df["tags"] = df["tags"].fillna("")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)

    # Calculate approval rating
    if "positive_ratings" in df.columns and "negative_ratings" in df.columns:
        total = df["positive_ratings"] + df["negative_ratings"]
        df["approval_rate"] = (df["positive_ratings"] / total.replace(0, 1)).round(2)

    print(f"[ETL] Clean dataset: {len(df)} records, {len(df.columns)} columns.")
    return df


def load(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    print(f"[ETL] Saved clean data to {path}")


def run():
    if not os.path.exists(RAW_PATH):
        print(f"[ETL] Raw file not found at {RAW_PATH}. Please download the Steam dataset first.")
        print("[ETL] You can get it from: https://www.kaggle.com/datasets/nikdavis/steam-store-games")
        return
    df = extract(RAW_PATH)
    df = transform(df)
    load(df, CLEAN_PATH)
    print("[ETL] Pipeline completed successfully.")


if __name__ == "__main__":
    run()
