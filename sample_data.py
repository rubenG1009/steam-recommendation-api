"""
sample_data.py — Generates a realistic Steam dataset in memory
No CSV needed. Used for deployment on Render.
"""

import pandas as pd

GAMES = [
    {"appid": 570,    "name": "Dota 2",               "genres": "Action;Strategy",         "tags": "MOBA;Strategy;Action",           "positive_ratings": 1200000, "negative_ratings": 250000,  "price": 0.0,  "release_date": "2013-07-09", "developer": "Valve"},
    {"appid": 730,    "name": "Counter-Strike 2",      "genres": "Action;FPS",              "tags": "FPS;Shooter;Competitive",        "positive_ratings": 900000,  "negative_ratings": 400000,  "price": 0.0,  "release_date": "2023-09-27", "developer": "Valve"},
    {"appid": 440,    "name": "Team Fortress 2",       "genres": "Action;FPS",              "tags": "FPS;Shooter;Free to Play",       "positive_ratings": 700000,  "negative_ratings": 80000,   "price": 0.0,  "release_date": "2007-10-10", "developer": "Valve"},
    {"appid": 271590, "name": "GTA V",                 "genres": "Action;Adventure",        "tags": "Open World;Action;Multiplayer",  "positive_ratings": 1100000, "negative_ratings": 210000,  "price": 29.99,"release_date": "2015-04-14", "developer": "Rockstar Games"},
    {"appid": 1091500,"name": "Cyberpunk 2077",        "genres": "RPG;Action",              "tags": "RPG;Open World;Sci-fi",          "positive_ratings": 620000,  "negative_ratings": 140000,  "price": 59.99,"release_date": "2020-12-10", "developer": "CD Projekt Red"},
    {"appid": 292030, "name": "The Witcher 3",         "genres": "RPG;Adventure",           "tags": "RPG;Open World;Story Rich",      "positive_ratings": 980000,  "negative_ratings": 25000,   "price": 39.99,"release_date": "2015-05-18", "developer": "CD Projekt Red"},
    {"appid": 413150, "name": "Stardew Valley",        "genres": "RPG;Simulation",          "tags": "Farming;Relaxing;Indie",         "positive_ratings": 750000,  "negative_ratings": 12000,   "price": 14.99,"release_date": "2016-02-26", "developer": "ConcernedApe"},
    {"appid": 1245620,"name": "Elden Ring",            "genres": "Action;RPG",              "tags": "Souls-like;RPG;Difficult",       "positive_ratings": 670000,  "negative_ratings": 55000,   "price": 59.99,"release_date": "2022-02-25", "developer": "FromSoftware"},
    {"appid": 374320, "name": "Dark Souls III",        "genres": "Action;RPG",              "tags": "Souls-like;Difficult;Action",    "positive_ratings": 430000,  "negative_ratings": 28000,   "price": 59.99,"release_date": "2016-04-11", "developer": "FromSoftware"},
    {"appid": 1938090,"name": "Call of Duty MW3",      "genres": "Action;FPS",              "tags": "FPS;Shooter;Multiplayer",        "positive_ratings": 200000,  "negative_ratings": 180000,  "price": 69.99,"release_date": "2023-11-10", "developer": "Activision"},
    {"appid": 1086940,"name": "Baldur's Gate 3",       "genres": "RPG;Strategy",            "tags": "RPG;Turn-Based;Co-op",           "positive_ratings": 820000,  "negative_ratings": 18000,   "price": 59.99,"release_date": "2023-08-03", "developer": "Larian Studios"},
    {"appid": 1517290,"name": "Sekiro",                "genres": "Action;Adventure",        "tags": "Souls-like;Action;Difficult",    "positive_ratings": 310000,  "negative_ratings": 22000,   "price": 59.99,"release_date": "2019-03-22", "developer": "FromSoftware"},
    {"appid": 39210,  "name": "FINAL FANTASY XIV",     "genres": "RPG;MMO",                 "tags": "MMORPG;RPG;Anime",               "positive_ratings": 270000,  "negative_ratings": 30000,   "price": 39.99,"release_date": "2013-08-27", "developer": "Square Enix"},
    {"appid": 1174180,"name": "Red Dead Redemption 2", "genres": "Action;Adventure",        "tags": "Open World;Western;Story Rich",  "positive_ratings": 490000,  "negative_ratings": 42000,   "price": 59.99,"release_date": "2019-12-05", "developer": "Rockstar Games"},
    {"appid": 1716740,"name": "DAVE THE DIVER",        "genres": "Adventure;RPG",           "tags": "Indie;Relaxing;Management",      "positive_ratings": 95000,   "negative_ratings": 4000,    "price": 19.99,"release_date": "2023-06-28", "developer": "MINTROCKET"},
    {"appid": 48000,  "name": "LIMBO",                 "genres": "Indie;Platformer",        "tags": "Indie;Puzzle;Dark",              "positive_ratings": 120000,  "negative_ratings": 5000,    "price": 9.99, "release_date": "2011-08-02", "developer": "Playdead"},
    {"appid": 105600, "name": "Terraria",              "genres": "Action;Adventure;Indie",  "tags": "Sandbox;2D;Survival",            "positive_ratings": 870000,  "negative_ratings": 18000,   "price": 9.99, "release_date": "2011-05-16", "developer": "Re-Logic"},
    {"appid": 322330, "name": "Don't Starve Together", "genres": "Survival;Indie",          "tags": "Survival;Co-op;Dark",            "positive_ratings": 350000,  "negative_ratings": 20000,   "price": 14.99,"release_date": "2016-04-21", "developer": "Klei Entertainment"},
    {"appid": 252490, "name": "Rust",                  "genres": "Action;Survival",         "tags": "Survival;Multiplayer;Open World","positive_ratings": 520000,  "negative_ratings": 200000,  "price": 39.99,"release_date": "2018-02-08", "developer": "Facepunch Studios"},
    {"appid": 578080, "name": "PUBG",                  "genres": "Action;Battle Royale",    "tags": "Battle Royale;Shooter;Survival", "positive_ratings": 600000,  "negative_ratings": 380000,  "price": 29.99,"release_date": "2017-12-21", "developer": "PUBG Corporation"},
    {"appid": 1446780,"name": "Monster Hunter Rise",   "genres": "Action;RPG",              "tags": "Action;Co-op;RPG",               "positive_ratings": 185000,  "negative_ratings": 12000,   "price": 39.99,"release_date": "2022-01-12", "developer": "Capcom"},
    {"appid": 601150, "name": "Devil May Cry 5",       "genres": "Action;Adventure",        "tags": "Action;Hack and Slash;Story",    "positive_ratings": 160000,  "negative_ratings": 8000,    "price": 29.99,"release_date": "2019-03-08", "developer": "Capcom"},
    {"appid": 1888160,"name": "EA SPORTS FC 24",       "genres": "Sports;Simulation",       "tags": "Football;Sports;Multiplayer",    "positive_ratings": 90000,   "negative_ratings": 110000,  "price": 69.99,"release_date": "2023-09-29", "developer": "EA Sports"},
    {"appid": 1237970,"name": "Titanfall 2",           "genres": "Action;FPS",              "tags": "FPS;Parkour;Story Rich",         "positive_ratings": 130000,  "negative_ratings": 5000,    "price": 29.99,"release_date": "2016-10-28", "developer": "Respawn Entertainment"},
    {"appid": 1551360,"name": "Forza Horizon 5",       "genres": "Racing;Simulation",       "tags": "Racing;Open World;Driving",      "positive_ratings": 210000,  "negative_ratings": 25000,   "price": 59.99,"release_date": "2021-11-09", "developer": "Playground Games"},
]


def get_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(GAMES)
    total = df["positive_ratings"] + df["negative_ratings"]
    df["approval_rate"] = (df["positive_ratings"] / total).round(3)
    return df
