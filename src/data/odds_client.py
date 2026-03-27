import requests
from src.config.settings import settings

class OddsClient:
    def __init__(self):
        self.api_key = settings.ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def fetch_live_odds(self):
        """Obtiene las cuotas más recientes de la liga configurada."""
        url = f"{self.base_url}/{settings.DEFAULT_SPORT}/odds/"
        params = {
            'api_key': self.api_key,
            'regions': settings.REGIONS,
            'markets': settings.MARKETS,
            'oddsFormat': 'decimal'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Lanza error si la API falla
            return response.json()
        except Exception as e:
            print(f"Error al conectar con The Odds API: {e}")
            return []
