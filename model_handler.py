from models.neural import SentimentAnalyzer
from keras import backend


class ModelHandler:
    """
    Intermediary handler to keep model logic separate from the server
    """

    def __init__(self):
        self.model = SentimentAnalyzer()
        self.model.load_model()
        self.prob = 0

    def predict_sentiment(self, text):
        backend.clear_session()
        self.prob = self.model.predict_sentiment([text])[0][0]
        return self.prob

    def get_prob(self):
        return self.prob
