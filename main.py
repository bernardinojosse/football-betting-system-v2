import os
import sys
import json
from datetime import datetime

# Agregamos 'src' al sistema para que encuentre las carpetas nuevas
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# IMPORTACIONES BASADAS EN TU IMAGEN:
try:
    # De 'configuración' importamos settings
    from configuración.settings import settings
    # De 'datos' importamos el cliente de momios
    from datos.odds_client import OddsClient
    # De 'estrategia' (asegúrate que bankroll_mgmt.py esté ahí o ajusta el nombre)
    # Si no tienes el archivo de estrategia aún, comentamos esta línea:
    # from estrategia.bankroll_mgmt import BettingStrategy 
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    # Si falla una importación, el bot nos dirá exactamente cuál nombre no coincide
    sys.exit(1)

def guardar_historial(nuevos_datos):
    """Guarda los resultados en la carpeta 'datos' (fuera de src) o 'datos' (dentro)."""
    # Basado en tu imagen, usaremos la carpeta 'datos' de la raíz
    ruta = 'datos/historial.json'
    if not os.path.exists('datos'): os.makedirs('datos')
    
    historial = []
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except: historial = []
    
    historial.extend(nuevos_datos)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def run_bot():
    print(f"🚀 NUVI-CORE Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("❌ Faltan los Secrets de GitHub (ODDS_API_KEY).")
        return

    # Inicializar cliente de datos
    client = OddsClient()
    
    print("📡 Buscando momios en vivo...")
    partidos = client.fetch_live_odds()

    if not partidos:
        print("⚠️ No se encontraron partidos.")
        return

    hallazgos = []
    for p in partidos:
        try:
            home = p['home_team']
            if not p.get('bookmakers'): continue
            
            cuota = p['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            
            # Lógica simple de valor (Probabilidad estimada 58%)
            if (0.58 * cuota) > 1.05:
                print(f"✅ Valor detectado: {home} a cuota {cuota}")
                hallazgos.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "equipo": home,
                    "cuota": cuota
                })
        except: continue

    if hallazgos:
        guardar_historial(hallazgos)
        print(f"📂 {len(hallazgos)} apuestas guardadas.")

if __name__ == "__main__":
    run_bot()
