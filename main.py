import time
from src.config.settings import settings
from src.data.odds_client import OddsClient
from src.models.engine import PredictionEngine
from src.strategy.bankroll_mgmt import BettingStrategy
from src.monitoring.metrics import PerformanceTracker

def run_bot():
    print(f"--- {settings.PROJECT_NAME} CONEXIÓN REAL ---")
    
    # 1. Inicializar herramientas
    client = OddsClient()
    engine = PredictionEngine()
    strategy = BettingStrategy()
    tracker = PerformanceTracker()

    # 2. Obtener datos reales de The Odds API
    print(f"Obteniendo momios para: {settings.DEFAULT_SPORT}...")
    matches = client.fetch_live_odds()

    if not matches:
        print("No se encontraron partidos activos o la API Key es inválida.")
        return

    # 3. Procesar cada partido encontrado
    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']
        
        # Buscamos el primer 'bookmaker' (casa de apuestas) disponible
        if not match['bookmakers']: continue
        
        bookie = match['bookmakers'][0]
        outcomes = bookie['markets'][0]['outcomes']
        
        # Extraer cuotas: Local, Empate, Visitante
        # Nota: Asumimos que el índice 0 es el equipo local usualmente
        odds_home = next(o['price'] for o in outcomes if o['name'] == home_team)
        
        print(f"\nAnalizando: {home_team} vs {away_team}")
        print(f"Cuota en {bookie['title']}: {odds_home}")

        # --- Lógica de Predicción ---
        # Aquí normalmente usarías estadísticas de API-Football. 
        # Por ahora, usamos una probabilidad estimada (60% por ejemplo)
        probabilidad_estimada = 0.58 
        
        # --- Cálculo de Valor ---
        valor = strategy.calculate_value(probabilidad_estimada, odds_home)
        
        if valor > 0.05: # Si el valor es mayor al 5%
            monto_apuesta = strategy.kelly_criterion(probabilidad_estimada, odds_home, bankroll=1000)
            print(f"¡ALERTA DE APUESTA! Apostar ${monto_apuesta:.2f} a {home_team}")
            tracker.log_bet(match['id'], "Home", "Pendiente", monto_apuesta, 0)
        else:
            print("Sin valor suficiente para apostar.")

    print("\nAnálisis finalizado.")

if __name__ == "__main__":
    run_bot()
