class MetricsCollector:
    def __init__(self):
        self.total_predictions = 0
        self.correct_predictions = 0

    def record_prediction(self, is_correct):
        self.total_predictions += 1
        if is_correct:
            self.correct_predictions += 1
            
    def get_accuracy(self):
        if self.total_predictions == 0: return 0
        return self.correct_predictions / self.total_predictions
