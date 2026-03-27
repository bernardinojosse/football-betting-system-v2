import time
from src.config.settings import settings
from src.data.processor import DataProcessor
from src.models.engine import PredictionEngine
from src.strategy.bankroll_mgmt import BettingStrategy
from src.monitoring.metrics import PerformanceTracker

def run_bot():
    print(f"--- {settings.PROJECT_NAME} ACTIVADO ---")
    
    # Inicializar componentes
    processor = DataProcessor()
    engine = PredictionEngine()
    strategy = BettingStrategy()
    tracker = PerformanceTracker()

    # Simulación de flujo de trabajo
    print("Buscando partidos en vivo...")
    
    # Datos de ejemplo (Simulando lo que vendría de la API)
    match_data = {
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "home_exp_goals": 2.1,
        "away_exp_goals": 1.4,
        "odds": 2.10
    }

    # 1. Procesar
    print(f"Analizando: {match_data['home_team']} vs {match_data['away_team']}")
    
    # 2. Predecir
    prediction = engine.predict_score(match_data['home_exp_goals'], match_data['away_exp_goals'])
    prob_win = 0.55  # Probabilidad calculada por motor
    
    # 3. Estrategia
    value = strategy.calculate_value(prob_win, match_data['odds'])
    
    if value > 0:
        stake = strategy.kelly_criterion(prob_win, match_data['odds'], bankroll=1000)
        print(f"¡VALOR ENCONTRADO! Apostar: ${stake:.2f}")
        tracker.log_bet("M1", "Win", "Win", stake, stake * (match_data['odds'] - 1))
    else:
        print("No hay valor suficiente en este partido.")

    print(f"ROI Actual: {tracker.get_roi():.2%}")

if __name__ == "__main__":
    run_bot()
