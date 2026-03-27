import os
import json
import time
from datetime import datetime
from src.config.settings import settings
from src.data.odds_client import OddsClient
from src.models.engine import PredictionEngine
from src.strategy.bankroll_mgmt import BettingStrategy
from src.monitoring.metrics import PerformanceTracker

def save_history(new_records):
    """Guarda los hallazgos en el archivo JSON dentro de la carpeta data."""
    file_path = 'data/history.json'
    
    # Asegurar que la carpeta data existe
    if not os.path.exists('data'):
        os.makedirs('data')

    # Leer historial existente o crear uno nuevo
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, Exception):
            history = []
    else:
        history = []

    # Unir registros nuevos
    history.extend(new_records)

    # Guardar archivo actualizado
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Historial actualizado: {len(new_records)} nuevos registros guardados.")

def run_bot():
    print(f"🚀 Ejecutando {settings.PROJECT_NAME}...")
    print(f"⏰ Hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Inicializar herramientas
    client = OddsClient()
    engine = PredictionEngine()
    strategy = BettingStrategy()
    tracker = PerformanceTracker()

    # 2. Obtener cuotas reales de The Odds API
    print(f"📡 Conectando a The Odds API ({settings.DEFAULT_SPORT})...")
    matches = client.fetch_live_odds()

    if not matches:
        print("⚠️ No se recibieron datos de la API. Revisa tu API Key o el límite de créditos.")
        return

    found_opportunities = []

    # 3. Analizar cada partido
    for match in matches:
        home_team = match.get('home_team')
        away_team = match.get('away_team')
        
        # Saltamos si no hay casas de apuestas disponibles
        if not match.get('bookmakers'):
            continue
        
        # Extraemos cuotas del primer bookmaker (ej. Bet365 o Caliente)
        bookie = match['bookmakers'][0]
        market = bookie['markets'][0]
        outcomes = market['outcomes']
        
        try:
            # Obtenemos el precio para el equipo local (Home)
            odd_home = next(o['price'] for o in outcomes if o['name'] == home_team)
            
            # --- LÓGICA DE PREDICCIÓN (EJEMPLO) ---
            # En una versión avanzada, aquí engine.predict_score() usaría datos de API-Football.
            # Usaremos una probabilidad base del 55% (0.55) para detectar valor.
            probabilidad_modelo = 0.55 
            
            # --- CÁLCULO DE VALOR ---
            valor = strategy.calculate_value(probabilidad_modelo, odd_home)
            
            print(f"⚽ {home_team} vs {away_team} | Cuota: {odd_home} | Valor: {valor:.4f}")

            # 4. Decisión de apuesta (Si el valor es mayor al 5%)
            if valor > 0.05:
                # Calculamos el stake sugerido con una banca de 1000 unidades
                monto_sugerido = strategy.kelly_criterion(probabilidad_modelo, odd_home, bankroll=1000)
                
                print(f"   💰 ¡VALOR DETECTADO! Sugerencia: {monto_sugerido:.2f} unidades")
                
                found_opportunities.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "liga": settings.DEFAULT_SPORT,
                    "partido": f"{home_team} vs {away_team}",
                    "mercado": "Local (H2H)",
                    "cuota": odd_home,
                    "prob_estimada": probabilidad_modelo,
                    "valor_esperado": round(valor, 4),
                    "stake_kelly": round(monto_sugerido, 2),
                    "casa_apuestas": bookie['title']
                })

        except Exception as e:
            print(f"❌ Error procesando partido {home_team}: {e}")
            continue

    # 5. Persistencia de datos
    if found_opportunities:
        save_history(found_opportunities)
    else:
        print("ℹ️ No se encontraron apuestas con valor suficiente en esta corrida.")

if __name__ == "__main__":
    run_bot()
