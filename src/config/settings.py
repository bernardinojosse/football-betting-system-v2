import os

class Settings:
    PROJECT_NAME = "Football Betting System V2"
    LOG_FILE = "logs/betting_system.log"
    DATA_DIR = "data"
    
    # API Keys
    AF_API_KEY = os.getenv("AF_API_KEY", "TU_LLAVE_FOOTBALL_API")
    ODDS_API_KEY = os.getenv("ODDS_API_KEY", "TU_LLAVE_THE_ODDS_API")
    
    # Configuración de búsqueda
    # Deportes disponibles: 'soccer_mexico_ligamx', 'soccer_spain_la_liga', 'soccer_usa_mls'
    DEFAULT_SPORT = "soccer_mexico_ligamx" 
    REGIONS = "us" # Puedes usar 'eu', 'us', 'uk', 'au'
    MARKETS = "h2h" # Ganador, Empate, Visitante

settings = Settings()
