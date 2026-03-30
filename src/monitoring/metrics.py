import json
import os
from datetime import datetime

class PerformanceTracker:
    def __init__(self, data_file='data/rendimiento.json'):
        self.data_file = data_file
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Crea la carpeta de datos si no existe."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def track_metrics(partido, cuota, stake, resultado="pendiente"):
    """Wrapper function for tracking metrics."""
    tracker = PerformanceTracker()
    tracker.log_bet(partido, cuota, stake, resultado)
        datos = self._leer_datos()
        datos.append(registro)
        self._guardar_datos(datos)
        print(f"📊 Métrica registrada: {partido} @ {cuota}")

    def _leer_datos(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _guardar_datos(self, datos):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
