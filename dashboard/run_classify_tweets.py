# coding: utf-8
import pickle
from pymongo import MongoClient
from classify_tweets import generate_dataset, classify_data

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

    # get tweets count
    tweets_count = db.tweets.count()

    page_size = 100
    total_page = int(tweets_count / page_size)
    if tweets_count % page_size > 0:
        total_page = total_page + 1

    for index in range(0, total_page):
        print(index)
        start = index * page_size

        # get tweets
        tweets = db.tweets_copy.find({}).skip(start).limit(page_size)
        # create dataset
        dataset = generate_dataset(tweets)
        # Classify tweets by topic
        clf_topics = classify_data(model_topics, vocabulary, dataset)
        # Classify tweets by polarity
        clf_polarities = classify_data(model_polarities, vocabulary, dataset)

        x = 0
        tweets.rewind()
        for tweet in tweets:
            nvars = {
                "topic_id" : int(clf_topics[x]),
                "polarity_id" : int(clf_polarities[x]),
            }
            db.tweets.update_one( {'_id' : tweet['_id']}, {'$set' : nvars} )
            x = x + 1
