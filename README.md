# 🎮 Steam Game Recommendation API

> RESTful API built with FastAPI that serves game data and personalized recommendations from a Steam dataset of 100K+ records, processed through a full ETL pipeline.

Built as a real-world backend project covering API design, data engineering and recommendation logic — fully documented and ready to run locally.

---

## ✨ Features

- **Full ETL Pipeline** — Extract, clean and normalize 100K+ raw Steam records with Pandas
- **Game Search & Filtering** — Search by name, paginate results, fetch by AppID
- **Recommendation Engine** — Genre-based recommendations and item similarity scoring (Jaccard)
- **Dataset Statistics** — Top-rated games, overview stats, games by developer
- **Auto-generated Docs** — Swagger UI available at `/docs` out of the box with FastAPI

---

## 🏗️ Architecture

```
Raw CSV (Steam dataset)
        ↓
   etl.py  →  Extract · Clean · Normalize  →  steam_clean.csv
        ↓
   main.py (FastAPI)
        ├── /games         → Search & retrieve games
        ├── /recommend     → Genre-based & similarity recommendations  
        └── /stats         → Dataset overview & top-rated games
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/games/` | Paginated list of all games |
| GET | `/games/search?q=query` | Search games by name |
| GET | `/games/{appid}` | Get a game by Steam AppID |
| GET | `/recommend/by-genre?genre=Action` | Top-rated games by genre |
| GET | `/recommend/similar/{appid}` | Games similar to a given game |
| GET | `/stats/overview` | General dataset statistics |
| GET | `/stats/top-rated` | Highest-rated games |
| GET | `/stats/by-developer?developer=Valve` | Games by developer |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Steam dataset CSV — download from [Kaggle](https://www.kaggle.com/datasets/nikdavis/steam-store-games) and place it at `data/steam_raw.csv`

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/rubenG1009/steam-recommendation-api.git
cd steam-recommendation-api

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the ETL pipeline

```bash
# Process and clean the raw dataset (run once)
python etl.py
```

### Start the API

```bash
uvicorn main:app --reload
```

API running at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## 📂 Project Structure

```
.
├── main.py                  # FastAPI app & router registration
├── etl.py                   # ETL pipeline (Extract · Transform · Load)
├── requirements.txt
├── .gitignore
├── data/
│   ├── loader.py            # Cached data loader
│   └── steam_raw.csv        # Raw dataset (not tracked by git)
└── routers/
    ├── games.py             # /games endpoints
    ├── recommendations.py   # /recommend endpoints
    └── stats.py             # /stats endpoints
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

---

## 👤 Author

**Rubén García Revett** — [LinkedIn](https://www.linkedin.com/in/ruben-garcia-revett-b72312223/) · [GitHub](https://github.com/rubenG1009)
