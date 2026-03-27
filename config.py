import os

class Config:
    # Captura las llaves de los Secrets de GitHub
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    AF_API_KEY = os.getenv("AF_API_KEY")
    
    # Configuración de la API de Football
    BASE_URL = "https://v3.football.api-sports.io"
    
    # Configuración de entorno
    # Si no hay valor, usa 'INFO' por defecto para evitar errores
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Verificación de seguridad rápida
if not Config.ODDS_API_KEY or not Config.AF_API_KEY:
    print("⚠️ Error: Las API Keys no se detectaron en el entorno.")
