import os

class Config:
    """
    Configuración base que lee los Secrets de GitHub o variables de entorno.
    """
    # Se obtienen los valores de los Secrets que configuraste en GitHub
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    AF_API_KEY = os.getenv("AF_API_KEY")
    
    # URL base para API-Football
    BASE_URL = "https://v3.football.api-sports.io"
    
    # Configuración de registro (Logs)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validación simple para avisarte si faltan las llaves en la consola de GitHub
if not Config.ODDS_API_KEY:
    print("⚠️ ADVERTENCIA: La variable ODDS_API_KEY no está configurada en los Secrets.")

if not Config.AF_API_KEY:
    print("⚠️ ADVERTENCIA: La variable AF_API_KEY no está configurada en los Secrets.")
