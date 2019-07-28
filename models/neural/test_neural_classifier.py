import unittest
from models.neural import SentimentAnalyzer


class TestNeuralClassifier(unittest.TestCase):

    def test_predict_sentiment(self):
        model = SentimentAnalyzer()
        model.load_model()

        test_positive = [
            "Today was a great day!",
            "So awesome!",
            "This is pretty god",
            "Absolutely terrific!"
            ]

        test_negative = [
            "Today sucked so much.",
            "ugh that was awful",
            "terrible. Worst day of my life",
            "Yuck!"
            ]

        self.assertTrue(
            all(x > 0.5 for x in model.predict_sentiment(test_positive))
            )
        self.assertTrue(
            all(x <= 0.5 for x in model.predict_sentiment(test_negative))
            )
