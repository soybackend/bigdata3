from pymongo import MongoClient
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix
from pymongo import MongoClient

def get_preprocess_text(stopwords, text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    words = re.sub(r"[^A-Za-záéíóúÁÉÍÓÚñ]", " ", text).lower().split()
    text = [w for w in words if not w in stopwords]
    return " ".join(text)

def generate_training_dataset(tweets_classified):
    # load nltk data
    nltk.download('stopwords')
    # get spanish stopwords
    spanish_stopwords = set(stopwords.words('spanish'))

    tweet_texts = []
    tweet_topics = []
    tweet_polarities = []

    for tweet in tweets_classified:
        tweet_texts.append(get_preprocess_text(spanish_stopwords, tweet['text']))
        tweet_topics.append(tweet['topic_id'])
        tweet_polarities.append(tweet['polarity_id'])
    return [tweet_texts, tweet_topics, tweet_polarities]

def generate_dataset(tweets):
    # load nltk data
    nltk.download('stopwords')
    # get spanish stopwords
    spanish_stopwords = set(stopwords.words('spanish'))

    tweet_texts = []

    for tweet in tweets:
        tweet_texts.append(get_preprocess_text(spanish_stopwords, tweet['payload']))
    return [tweet_texts]

def classify_data(model, vocabulary, dataset):
    # create count vectorizer
    count_vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                                       preprocessor = None, stop_words = None,
                                       max_features = 2000, vocabulary = vocabulary)

    # create training dataset vectorizer
    dataset_vectorizer = count_vectorizer.transform(dataset[0]).toarray()
    return model.predict(dataset_vectorizer)
