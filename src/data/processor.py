import pandas as pd

class DataProcessor:
    def clean_match_data(self, raw_data):
        """Convierte la respuesta de la API en un formato limpio."""
        if not raw_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        # Filtramos solo columnas necesarias para el análisis
        columns = ['fixture', 'teams', 'goals', 'score']
        return df[df.columns.intersection(columns)]

    def get_team_form(self, team_id, last_matches):
        """Calcula la forma actual del equipo (últimos resultados)."""
        # Lógica para procesar rachas (W, D, L)
        return last_matches
