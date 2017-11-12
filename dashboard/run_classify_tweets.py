# coding: utf-8
import pickle
from pymongo import MongoClient
from classify_tweets import Classification

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    classifier = Classification()

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
        dataset = classifier.generate_dataset(tweets)
        # Classify tweets by topic
        clf_topics = classifier.classify_by_topic(dataset)
        # Classify tweets by polarity
        clf_polarities = classifier.classify_by_polarity(dataset)

        x = 0
        tweets.rewind()
        for tweet in tweets:
            nvars = {
                "topic_id" : int(clf_topics[x]),
                "polarity_id" : int(clf_polarities[x]),
            }
            db.tweets_copy.update_one( {'_id' : tweet['_id']}, {'$set' : nvars} )
            x = x + 1
