from predictor import FootballPredictor

def main():
    print("Iniciando Football Betting System V2...")
    predictor = FootballPredictor()
    # Ejemplo rápido
    res = predictor.predict_match("Real Madrid", "Barcelona", {})
    print(f"Predicción inicial: {res}")

if __name__ == "__main__":
    main()
