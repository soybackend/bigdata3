# coding: utf-8
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    # Replies
    replies = db.tweets.find({'tweet.in_reply_to_status_id_str': {'$ne' : None}})

    for rps in replies:
        original_id = rps['tweet']['in_reply_to_status_id_str']
        original = db.tweets.find_one({'tweet.id_str': original_id})

        if original:
            reply = {
                "reply_id" : rps['tweet']['id_str'],
                "reply_text" : rps['tweet']['text'],
                "reply_user_id" : rps['tweet']['user']['id_str'],
                "reply_username" : rps['tweet']['user']['screen_name'],
                "reply_location" : rps['tweet']['user']['location'],
                "reply_topic_id" : rps['topic_id'],
                "reply_topic_name" : rps['topic_name'],
                "reply_polarity_id" : rps['polarity_id'],
                "reply_polarity" : rps['polarity'],

                "original_id" : rps['tweet']['in_reply_to_status_id_str'],
                "original_user_id" : rps['tweet']['in_reply_to_user_id_str'],
                "original_username" : rps['tweet']['in_reply_to_screen_name'],
                "original_text" : original['tweet']['text'],
                "original_location" : original['tweet']['user']['location'],
                "original_topic_id" : original['topic_id'],
                "original_polarity_id" : original['polarity_id'],
                "original_topic_name" : original['topic_name'],
                "original_polarity" : original['polarity'],
            }
            if reply['reply_username'] != reply['original_username']:
                print(original_id)
                db.tweets_replies.insert_one(reply)
