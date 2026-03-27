import os
import json
import time
from datetime import datetime
# Importamos la configuración desde el archivo de la raíz
try:
    from config import Config
except ImportError:
    # Si falla la importación, definimos una clase mínima para evitar el crash
    class Config:
        ODDS_API_KEY = os.getenv("ODDS_API_KEY")
        AF_API_KEY = os.getenv("AF_API_KEY")
        DEFAULT_SPORT = "soccer_mexico_ligamx"

# Importación de módulos internos
from src.data.odds_client import OddsClient
from src.models.engine import PredictionEngine
from src.strategy.bankroll_mgmt import BettingStrategy
from src.monitoring.metrics import PerformanceTracker

def save_history(new_records):
    """Guarda los hallazgos en data/history.json de forma segura."""
    file_path = 'data/history.json'
    
    if not os.path.exists('data'):
        os.makedirs('data')

    history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []

    history.extend(new_records)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    print(f"✅ Se guardaron {len(new_records)} registros nuevos.")

def run_bot():
    print(f"🚀 NUVI-CORE V2 | Iniciando ejecución: {datetime.now()}")
    
    # 1. Validación de Credenciales
    if not Config.ODDS_API_KEY:
        print("❌ ERROR: No se encontró ODDS_API_KEY. Revisa los Secrets de GitHub.")
        return

    # 2. Inicialización
    client = OddsClient()
    engine = PredictionEngine()
    strategy = BettingStrategy()
    tracker = PerformanceTracker()

    # 3. Obtener Datos Reales
    print(f"📡 Conectando a The Odds API para: {Config.DEFAULT_SPORT}...")
    matches = client.fetch_live_odds()

    if not matches:
        print("⚠️ No hay partidos disponibles o error de conexión.")
        return

    opportunities = []

    # 4. Procesamiento y Análisis
    for match in matches:
        try:
            home = match['home_team']
            away = match['away_team']
            
            if not match.get('bookmakers'): continue
            
            # Extraer la cuota del equipo local (Home)
            outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
            odd_home = next(o['price'] for o in outcomes if o['name'] == home)
            
            # --- MODELO DE PREDICCIÓN ---
            # Probabilidad base (puedes subirla al 60% para ser más exigente)
            prob_modelo = 0.58 
            
            # --- CÁLCULO DE VALOR ---
            valor = strategy.calculate_value(prob_modelo, odd_home)
            
            if valor > 0.05: # Valor mayor al 5%
                stake = strategy.kelly_criterion(prob_modelo, odd_home, bankroll=1000)
                
                opportunities.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "partido": f"{home} vs {away}",
                    "cuota": odd_home,
                    "valor": round(valor, 4),
                    "stake_sugerido": round(stake, 2)
                })
                print(f"✨ VALOR ENCONTRADO: {home} @ {odd_home}")

        except Exception as e:
            print(f"⚠️ Error analizando partido: {e}")
            continue

    # 5. Guardado Final
    if opportunities:
        save_history(opportunities)
    else:
        print("ℹ️ No se detectaron oportunidades de apuesta en esta jornada.")

if __name__ == "__main__":
    run_bot()
