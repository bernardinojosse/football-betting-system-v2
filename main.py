import os
import json
import time
from src.config.settings import settings
from src.data.odds_client import OddsClient
from src.models.engine import PredictionEngine
from src.strategy.bankroll_mgmt import BettingStrategy
from src.monitoring.metrics import PerformanceTracker

def run_bot():
    print(f"--- {settings.PROJECT_NAME} | INICIO DE EJECUCIÓN ---")
    print(f"Fecha/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Inicializar Componentes
    client = OddsClient()
    engine = PredictionEngine()
    strategy = BettingStrategy()
    tracker = PerformanceTracker()

    # 2. Obtener datos reales de The Odds API
    print(f"Consultando cuotas para: {settings.DEFAULT_SPORT}...")
    matches = client.fetch_live_odds()

    if not matches:
        print("No se obtuvieron partidos. Revisa tu API Key o la conexión.")
        return

    findings = [] # Para guardar en el historial

    # 3. Procesar cada partido encontrado
    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']
        
        # Verificar si hay casas de apuestas disponibles
        if not match['bookmakers']:
            continue
        
        # Tomamos la primera casa de apuestas (puedes filtrar por una específica)
        bookie = match['bookmakers'][0]
        outcomes = bookie['markets'][0]['outcomes']
        
        try:
            # Obtener el precio (cuota) del equipo local
            odd_home = next(o['price'] for o in outcomes if o['name'] == home_team)
            
            # --- LÓGICA DE PREDICCIÓN ---
            # Probabilidad base (Este valor debería venir de tus stats de API-Football)
            # Por ahora usamos 0.55 (55%) como ejemplo de prueba
            prob_estimada = 0.55 
            
            # --- CÁLCULO DE VALOR ---
            valor = strategy.calculate_value(prob_estimada, odd_home)
            
            print(f"[{home_team} vs {away_team}] Cuota: {odd_home} | Valor: {valor:.2f}")

            # 4. Decisión de Apuesta
            if valor > 0.05: # Si hay más del 5% de ventaja
                stake = strategy.kelly_criterion(prob_estimada, odd_home, bankroll=1000)
                print(f"  >>> ¡APUESTA RECOMENDADA! Monto: ${stake:.2f}")
                
                # Registro para el historial
                findings.append({
                    "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "partido": f"{home_team} vs {away_team}",
                    "pick": home_team,
                    "cuota": odd_home,
                    "valor_detectado": round(valor, 4),
                    "stake_sugerido": round(stake, 2)
                })
        except Exception as e:
            print(f"Error procesando {home_team}: {e}")
            continue

    # 5. GUARDAR RESULTADOS (Crítico para GitHub Actions)
    if findings:
        save_history(findings)
    else:
        print("No se encontraron oportunidades de valor en esta corrida.")

def save_history(new_data):
    file_path = 'data/history.json'
    
    # Asegurar que la carpeta data existe
    if not os.path.exists('data'):
        os.makedirs('data')

    # Leer historial existente
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
    except Exception:
        history = []

    # Añadir nuevos hallazgos
    history.extend(new_data)

    # Guardar de nuevo
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    print(f"Se guardaron {len(new_data)} registros en {file_path}")

if __name__ == "__main__":
    run_bot()
