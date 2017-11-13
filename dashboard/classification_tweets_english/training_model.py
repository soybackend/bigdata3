# coding: utf-8
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
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
    en_stopwords = set(stopwords.words('english'))

    tweet_texts = []
    tweet_polarities = []

    for tweet in tweets_classified:
        tweet_texts.append(get_preprocess_text(en_stopwords, tweet['text']))
        tweet_polarities.append(tweet['polarity_id'])
    return [tweet_texts, tweet_polarities]

def build_classification_model(training_dataset):
    # create count vectorizer
    count_vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                                       preprocessor = None, stop_words = None,
                                       max_features = 2000)
    # create training dataset vectorizer
    training_dataset_vectorizer = count_vectorizer.fit_transform(
                                        training_dataset[0]).toarray()

    # Save vocabulary
    vocab = count_vectorizer.get_feature_names()
    filename_vocabulary = '../classification_models/tweets_english.vocabulary'
    pickle.dump(vocab, open(filename_vocabulary, 'wb'))

    # Naive Bayes - training
    model_polarities = MultinomialNB()
    model_polarities = model_polarities.fit(training_dataset_vectorizer, training_dataset[1])

    # save the model to disk
    filename_model_polarities = '../classification_models/naive_bayes_polarities_english.model'
    pickle.dump(model_polarities, open(filename_model_polarities, 'wb'))

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    # get tweets classified
    tweets_classified = db.tweets_classified_dataset_english.find({}).limit(10000)

    # create training dataset
    training_dataset = generate_training_dataset(tweets_classified)

    # create classification models (topic and polarity)
    build_classification_model(training_dataset)
