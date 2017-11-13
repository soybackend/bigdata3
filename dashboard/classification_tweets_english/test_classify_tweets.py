# coding: utf-8
import pickle
import re
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
    english_stopwords = set(stopwords.words('english'))

    tweet_texts = []
    tweet_polarities = []

    for tweet in tweets_classified:
        tweet_texts.append(get_preprocess_text(english_stopwords, tweet['text']))
        tweet_polarities.append(tweet['polarity_id'])
    return [tweet_texts, tweet_polarities]

def classify_by_polarity(model_polarities, dataset):
    # create training dataset vectorizer
    dataset_vectorizer = count_vectorizer.transform(dataset[0]).toarray()
    return model_polarities.predict(dataset_vectorizer)


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    # load vocabulary
    filename_vocabulary = '../classification_models/tweets_english.vocabulary'
    vocabulary = pickle.load(open(filename_vocabulary, 'rb'))

    filename_model_polarities = '../classification_models/naive_bayes_polarities_english.model'
    model_polarities = pickle.load(open(filename_model_polarities, 'rb'))

    # create count vectorizer
    count_vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                                       preprocessor = None, stop_words = None,
                                       max_features = 2000, vocabulary = vocabulary)

    # get tweets classified
    tweets = db.tweets_classified_dataset_english.find({}).skip(0).limit(50)

    # create dataset
    dataset = generate_training_dataset(tweets)

    # Classify tweets by polarity
    clf_polarities = classify_by_polarity(model_polarities, dataset)

    result_bayes = clf_polarities
    data_test = dataset[1]
    print(result_bayes)
    print(data_test)
    precision, recall, fscore, support = score(data_test, result_bayes, labels=[-1, 0 ,1], average='micro')
    # Calculate performance metrics for Naive Bayes classifier
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    #
    # Calculate confusion matrix for Naive Bayes classifier
    print(confusion_matrix(data_test, result_bayes, labels=[-1, 0, 1]))
