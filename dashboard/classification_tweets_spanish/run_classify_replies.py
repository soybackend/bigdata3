# coding: utf-8
import pickle
from pymongo import MongoClient

import sys
sys.path.append('../')
from classify_tweets import *

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    classifier = Classification()

    # get tweets count
    replies_count = db.replies.count()

    page_size = 100
    total_page = int(replies_count / page_size)
    if replies_count % page_size > 0:
        total_page = total_page + 1

    for index in range(0, total_page):
        print(index)
        start = index * page_size

        # get replies
        replies = db.replies.find({}).skip(start).limit(page_size)
        # create dataset (reply)
        dataset = classifier.generate_dataset_replies(replies)
        replies.rewind()
        # create dataset (original)
        dataset_orig = classifier.generate_dataset_replies_original(replies)
        # Classify replies by topic
        clf_topics = classifier.classify_by_topic(dataset)
        # Classify replies by polarity
        clf_polarities = classifier.classify_by_polarity(dataset)

        # Classify original by topic
        clf_topics_orig = classifier.classify_by_topic(dataset_orig)
        # Classify original by polarity
        clf_polarities_orig = classifier.classify_by_polarity(dataset_orig)

        x = 0
        replies.rewind()
        for reply in replies:
            topic_id = int(clf_topics[x])
            polarity_id = int(clf_polarities[x])
            topic_orig_id = int(clf_topics_orig[x])
            polarity_orig_id = int(clf_polarities_orig[x])
            support_score = polarity_id - polarity_orig_id
            data = {
                "reply_id" : reply['reply_id'],
                "reply_text" : reply['reply_text'],
                "reply_username" : reply['reply_username'],
                "reply_location" : reply['reply_location'],
                "reply_topic_id" : topic_id,
                "reply_topic_name" : classifier.get_topic(topic_id),
                "reply_polarity_id" : polarity_id,
                "reply_polarity" : classifier.get_polarity(polarity_id),
                "original_id" : reply['original_id'],
                "original_username" : reply['original_username'],
                "original_text" : reply['original_text'],
                "original_location" : reply['original_location'],
                "original_topic_id" : topic_orig_id,
                "original_topic_name" : classifier.get_topic(topic_orig_id),
                "original_polarity_id" : polarity_orig_id,
                "original_polarity" : classifier.get_polarity(polarity_orig_id),
                "support_score" : support_score,
            }
            db.tweets_replies.insert_one(data)
            x = x + 1
