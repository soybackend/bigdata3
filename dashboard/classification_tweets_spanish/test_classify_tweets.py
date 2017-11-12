# coding: utf-8
import pickle
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix
from pymongo import MongoClient

import sys
sys.path.append('../')
from classify_tweets import *

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    classifier = Classification()

    # get tweets classified
    tweets = db.tweets_classified_test.find({})

    # create dataset
    dataset = classifier.generate_training_dataset(tweets)

    # Classify tweets by topic
    clf_topics = classifier.classify_by_topic(dataset)

    # Classify tweets by polarity
    clf_polarities = classifier.classify_by_polarity(dataset)

    result_bayes = clf_topics
    data_test = dataset[1]
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
