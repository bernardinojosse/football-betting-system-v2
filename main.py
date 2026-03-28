import os
import sys
import json
from datetime import datetime

# Obligamos a Python a mirar dentro de 'src'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))

# IMPORTACIONES SIN ACENTOS
try:
    # Cambiamos 'configuración' por 'configuracion'
    from configuracion.settings import settings
    from datos.odds_client import OddsClient
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de haber renombrado la carpeta 'configuración' a 'configuracion' (sin acento).")
    sys.exit(1)

def guardar_resultado(datos_nuevos):
    """Guarda en la carpeta datos de la raíz."""
    ruta = 'datos/historial.json'
    if not os.path.exists('datos'):
        os.makedirs('datos')
    
    historial = []
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except:
            historial = []
    
    historial.extend(datos_nuevos)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def run_bot():
    print(f"🚀 Ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validar API Key directamente del entorno de GitHub
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("❌ ERROR: Configura el Secret 'ODDS_API_KEY' en GitHub.")
        return

    client = OddsClient()
    
    print("📡 Consultando The Odds API...")
    try:
        partidos = client.fetch_live_odds()
    except Exception as e:
        print(f"❌ Error al llamar a la API: {e}")
        return

    if not partidos:
        print("⚠️ No hay partidos disponibles.")
        return

    oportunidades = []
    for p in partidos:
        try:
            home = p.get('home_team')
            if not p.get('bookmakers'): continue
            
            # Cuota decimal
            cuota = p['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            
            # Si el valor esperado es positivo (usando 58% como base)
            if (0.58 * cuota) > 1.05:
                print(f"✅ ¡VALOR! {home} a cuota {cuota}")
                oportunidades.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "partido": f"{home} vs {p.get('away_team')}",
                    "cuota": cuota
                })
        except:
            continue

    if oportunidades:
        guardar_resultado(oportunidades)
        print(f"📂 Guardadas {len(oportunidades)} posibles apuestas.")

if __name__ == "__main__":
    run_bot()
