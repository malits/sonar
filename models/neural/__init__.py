import re

import dill as pkl
from gensim.models.word2vec import Word2Vec
from keras import Sequential
# from keras.layers import Dense, Activation
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale

STOPWORDS = set(stopwords.words('english'))

not_stops = ["but", "very", "most", "nor", "no", "against"]

for stop in not_stops:
    STOPWORDS.remove(stop)

contractions = {
        "ain't": "am not / are not / is not / has not / have not",
        "aren't": "are not / am not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he had / he would",
        "he'd've": "he would have",
        "he'll": "he shall / he will",
        "he'll've": "he shall have / he will have",
        "he's": "he has / he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how has / how is / how does",
        "I'd": "I had / I would",
        "I'd've": "I would have",
        "I'll": "I shall / I will",
        "I'll've": "I shall have / I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had / it would",
        "it'd've": "it would have",
        "it'll": "it shall / it will",
        "it'll've": "it shall have / it will have",
        "it's": "it has / it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she had / she would",
        "she'd've": "she would have",
        "she'll": "she shall / she will",
        "she'll've": "she shall have / she will have",
        "she's": "she has / she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so as / so is",
        "that'd": "that would / that had",
        "that'd've": "that would have",
        "that's": "that has / that is",
        "there'd": "there had / there would",
        "there'd've": "there would have",
        "there's": "there has / there is",
        "they'd": "they had / they would",
        "they'd've": "they would have",
        "they'll": "they shall / they will",
        "they'll've": "they shall have / they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had / we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what shall / what will",
        "what'll've": "what shall have / what will have",
        "what're": "what are",
        "what's": "what has / what is",
        "what've": "what have",
        "when's": "when has / when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where has / where is",
        "where've": "where have",
        "who'll": "who shall / who will",
        "who'll've": "who shall have / who will have",
        "who's": "who has / who is",
        "who've": "who have",
        "why's": "why has / why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had / you would",
        "you'd've": "you would have",
        "you'll": "you shall / you will",
        "you'll've": "you shall have / you will have",
        "you're": "you are",
        "you've": "you have"
        }


class SentimentAnalyzer:
    '''
    Neural model for sentiment analysis
    '''

    def __init__(self):
        self.ndims = 200

    def load_model(self):
        '''
        Loads necessary pickle files for the model
        '''
        self.classifier: Sequential = pkl.load(
            open("data/sentiment_classifier00.pkl", "rb"))
        self.word2vec: Word2Vec = pkl.load(open("data/tweet_w2v00.pkl", "rb"))
        self.tfidf: np.array = pkl.load(open("data/tfidf_lookup00.pkl", "rb"))
        self.tokenizer: TweetTokenizer = pkl.load(
            open("data/tweet_tokenizer00.pkl", "rb")
            )

    def tokenize(self, tweet: str) -> [str]:
        '''
        :param tweet: tweet to be tokenized
        :returns tokens: a list of processed tweets
        '''
        sub_regex = r'(#[A-Za-z0-9])|(https)|[\?!\.,]'
        tweet = str(tweet)
        tokens = self.tokenizer.tokenize(tweet)
        tokens = [re.sub(sub_regex, '', t) for t in tokens]
        tokens = [t.lower() for t in tokens if t is not None and t != '']
        tokens = [self.expand_contractions(t) for t in tokens]
        tokens = [t for t in tokens if t not in STOPWORDS]
        return tokens

    def expand_contractions(self, text: str) -> str:
        '''
        :param text: contraction text to be expanded
        :returns text: expanded contraction
        '''
        if text in contractions.keys():
            return contractions[text]
        return text

    def create_tweet_vector(self, words: [str]) -> np.array:
        '''
        :param words: list of tweet tokens
        :returns vector: numpy array of vectorized tweets
        '''
        vector = np.zeros((1, self.ndims))
        count = 0

        for w in words:
            try:
                vector += self.word2vec.wv[w].reshape((1, self.ndims))  \
                                    * self.tfidf[w]
                count += 1
            except KeyError:
                continue

        if count != 0:
            return np.divide(vector, count)
        else:
            return vector

    # TODO: refactor params here
    def predict_sentiment(self, texts: [str]) -> np.array:
        '''
        :param texts: Array of texts
        :returns corresponding numpy array of sentiment prediction
        '''
        texts = [self.tokenize(text) for text in texts]
        tweet_vectors = np.concatenate(
            [self.create_tweet_vector(text) for text in texts]
        )
        tweet_vectors = scale(tweet_vectors, axis=1)
        return self.classifier.predict(tweet_vectors)
