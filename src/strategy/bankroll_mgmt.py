class BettingStrategy:
    def calculate_value(self, probability, odds):
        """Calcula si una apuesta tiene valor esperado positivo."""
        # Valor = (Probabilidad * Cuota) - 1
        value = (probability * odds) - 1
        return value

    def kelly_criterion(self, probability, odds, bankroll):
        """Calcula cuánto apostar según el criterio de Kelly."""
        b = odds - 1
        p = probability
        q = 1 - p
        fraction = (b * p - q) / b
        # Usamos 'Fractional Kelly' (0.1) para ser conservadores
        return max(0, bankroll * fraction * 0.1)
