# coding: utf-8
import pickle
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix
from pymongo import MongoClient
from classify_tweets import generate_training_dataset, classify_data

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    # load vocabulary
    filename_vocabulary = 'classification_models/tweets.vocabulary'
    vocabulary = pickle.load(open(filename_vocabulary, 'rb'))

    # load the model from disk
    filename_model_topics = 'classification_models/naive_bayes_topics.model'
    model_topics = pickle.load(open(filename_model_topics, 'rb'))

    filename_model_polarities = 'classification_models/naive_bayes_polarities.model'
    model_polarities = pickle.load(open(filename_model_polarities, 'rb'))

    # get tweets classified
    tweets = db.tweets_classified_test.find({})

    # create dataset
    dataset = generate_training_dataset(tweets)

    # Classify tweets by topic
    clf_topics = classify_data(model_topics, vocabulary, dataset)

    # Classify tweets by polarity
    clf_polarities = classify_data(model_polarities, vocabulary, dataset)

    result_bayes = clf_polarities
    data_test = dataset[2]
    print(result_bayes)
    print(data_test)
    precision, recall, fscore, support = score(data_test, result_bayes, labels=[-1, 0 ,1])
    # Calculate performance metrics for Naive Bayes classifier
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    #
    # Calculate confusion matrix for Naive Bayes classifier
    print(confusion_matrix(data_test, result_bayes, labels=[-1, 0, 1]))
