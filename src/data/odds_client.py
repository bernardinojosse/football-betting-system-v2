import requests
from src.config.settings import settings

class OddsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def get_live_odds(self, sport="soccer_mexico_ligamx", region="us"):
        """Obtiene momios en vivo para una liga específica."""
        url = f"{self.base_url}/{sport}/odds/"
        params = {
            'api_key': self.api_key,
            'regions': region, # 'us' o 'eu'
            'markets': 'h2h',  # Local, Empate, Visitante
            'oddsFormat': 'decimal'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
