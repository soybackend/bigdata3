from pymongo import MongoClient
import os
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


class Classification():

    # load vocabulary
    filename_vocabulary = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       'classification_models/tweets.vocabulary')
    vocabulary = pickle.load(open(filename_vocabulary, 'rb'))

    # load the model from disk
    filename_model_topics = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                         'classification_models/naive_bayes_topics.model')
    model_topics = pickle.load(open(filename_model_topics, 'rb'))

    filename_model_polarities = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'classification_models/naive_bayes_polarities.model')
    model_polarities = pickle.load(open(filename_model_polarities, 'rb'))

    # create count vectorizer
    count_vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                                       preprocessor = None, stop_words = None,
                                       max_features = 2000, vocabulary = vocabulary)

    def __init__(self):
        pass

    def get_preprocess_text(self, stopwords, text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@\S+", "", text)
        words = re.sub(r"[^A-Za-záéíóúÁÉÍÓÚñ]", " ", text).lower().split()
        text = [w for w in words if not w in stopwords]
        return " ".join(text)

    def generate_training_dataset(self, tweets_classified):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        tweet_texts = []
        tweet_topics = []
        tweet_polarities = []

        for tweet in tweets_classified:
            tweet_texts.append(self.get_preprocess_text(spanish_stopwords, tweet['text']))
            tweet_topics.append(tweet['topic_id'])
            tweet_polarities.append(tweet['polarity_id'])
        return [tweet_texts, tweet_topics, tweet_polarities]

    def generate_dataset(self, tweets):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        tweet_texts = []

        for tweet in tweets:
            tweet_texts.append(self.get_preprocess_text(spanish_stopwords, tweet['payload']))
        return [tweet_texts]

    def generate_dataset_single_text(self, text):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        tweet_texts = []
        tweet_texts.append(self.get_preprocess_text(spanish_stopwords, text))
        return [tweet_texts]

    def classify_by_topic(self, dataset):
        # create training dataset vectorizer
        dataset_vectorizer = self.count_vectorizer.transform(dataset[0]).toarray()
        return self.model_topics.predict(dataset_vectorizer)

    def classify_by_polarity(self, dataset):
        # create training dataset vectorizer
        dataset_vectorizer = self.count_vectorizer.transform(dataset[0]).toarray()
        return self.model_polarities.predict(dataset_vectorizer)

    def get_topic(self, key):
        topic = 'Sin clasificar'
        if key == 0:
            topic = 'otro'
        elif key == 1:
            topic = 'proceso de paz'
        elif key == 2:
            topic = 'electoral'
        elif key == 3:
            topic = 'corrupción'
        return topic

    def get_polarity(self, key):
        polarity = 'Sin clasificar'
        if key == 1:
            polarity = 'negativo'
        elif key == 2:
            polarity = 'casi negativo'
        elif key == 3:
            polarity = 'neutro'
        elif key == 4:
            polarity = 'casi positivo'
        elif key == 5:
            polarity = 'positivo'
        return polarity
