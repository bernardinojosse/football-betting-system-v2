import os

class Settings:
    PROJECT_NAME = "Football Betting System V2"
    # Las llaves se leen del entorno (GitHub Secrets o Docker)
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    AF_API_KEY = os.getenv("AF_API_KEY")
    
    DEFAULT_SPORT = "soccer_mexico_ligamx"
    REGIONS = ['us']
    MARKETS = ['h2h']
    DATA_DIR = "data"
    HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

settings = Settings()