class FootballPredictor:
    def __init__(self, model_type="poisson"):
        self.model_type = model_type

    def predict_match(self, home_team, away_team, stats):
        return {
            "match": f"{home_team} vs {away_team}",
            "home_win_prob": 0.45,
            "draw_prob": 0.25,
            "away_win_prob": 0.30
        }
