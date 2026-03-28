import os
import sys
import json
from datetime import datetime

# Add 'src' to the system path to find the modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))

# SAFE IMPORTS (English names)
try:
    from config.settings import settings
    from data.odds_client import OddsClient
    from monitoring.metrics import PerformanceTracker
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Check if your folders are named 'config', 'data', and 'monitoring' (no accents).")
    sys.exit(1)

def save_to_history(new_data):
    """Saves findings to the root data folder."""
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
    
    history.extend(new_data)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def run_bot():
    print(f"🚀 NUVI-CORE V2 Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validate API Key from GitHub Secrets
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("❌ ERROR: ODDS_API_KEY not found in GitHub Secrets.")
        return

    # Initialize components
    client = OddsClient()
    tracker = PerformanceTracker()
    
    print("📡 Fetching live odds from API...")
    try:
        matches = client.fetch_live_odds()
    except Exception as e:
        print(f"❌ API Call failed: {e}")
        return

    if not matches:
        print("⚠️ No matches found at this time.")
        return

    opportunities = []
    for m in matches:
        try:
            home_team = m.get('home_team')
            if not m.get('bookmakers'): continue
            
            # Get the first available decimal odd
            current_odd = m['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            
            # Value Logic (Estimated 58% probability)
            if (0.58 * current_odd) > 1.05:
                print(f"✅ VALUE FOUND: {home_team} @ {current_odd}")
                opportunities.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "match": f"{home_team} vs {m.get('away_team')}",
                    "odd": current_odd
                })
                # Log to our performance tracker
                tracker.log_bet(home_team, current_odd, stake=10.0)
        except:
            continue

    if opportunities:
        save_to_history(opportunities)
        print(f"📂 Saved {len(opportunities)} opportunities to history.json")

if __name__ == "__main__":
    run_bot()
