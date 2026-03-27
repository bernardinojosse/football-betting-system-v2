import math

class PredictionEngine:
    def poisson_probability(self, actual_goals, expected_goals):
        """Calcula la probabilidad de que ocurra un número X de goles."""
        e_neg_mu = math.exp(-expected_goals)
        mu_pow_x = math.pow(expected_goals, actual_goals)
        factorial_x = math.factorial(actual_goals)
        return (e_neg_mu * mu_pow_x) / factorial_x

    def predict_score(self, home_exp_goals, away_exp_goals):
        """Genera una matriz de probabilidades para el marcador exacto."""
        # Simplificado para retornar el marcador más probable
        return {
            "predicted_home_goals": round(home_exp_goals),
            "predicted_away_goals": round(away_exp_goals)
        }
