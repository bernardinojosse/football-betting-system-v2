import os

class Settings:
    PROJECT_NAME = "Football Betting System V2"
    LOG_FILE = os.getenv("LOG_FILE", "logs/betting_system.log")
    DATA_DIR = os.getenv("DATA_DIR", "data")
    HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

settings = Settings()
