import os

class Config:
    # Captura las llaves de GitHub Secrets
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    AF_API_KEY = os.getenv("AF_API_KEY")
    
    # Configuraciones por defecto
    BASE_URL = "https://v3.football.api-sports.io"
    DEFAULT_SPORT = "soccer_mexico_ligamx"
    
    @classmethod
    def validate(cls):
        if not cls.ODDS_API_KEY:
            print("❌ ERROR: ODDS_API_KEY no encontrada en Secrets de GitHub.")
            return False
        if not cls.AF_API_KEY:
            print("❌ ERROR: AF_API_KEY no encontrada en Secrets de GitHub.")
            return False
        return True

# Esto facilita la importación en otros archivos
config = Config()
