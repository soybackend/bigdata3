#!/usr/bin/env python
import sys
import json
import time
import logging
import twitter
import urllib.parse

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter']

from os import environ as e

t = twitter.Api(
    consumer_key="",
    consumer_secret="",
    access_token_key="",
    access_token_secret="",

    sleep_on_rate_limit=True
)

users = [
    # "JuanLozano_R",
    # "RafaelPardo",
    # "ernestosamperp"
    # "AndresPastrana_",
    # "RestrepoJCamilo",
    # "CristoBustos",
    # "HoracioSerpa",
    # "alejogiral",
    # "Rodrigo_Lara_",
    # "carlosfgalan",
    # "AABenedetti",
    # "JuanManSantos",
    # "CGurisattiNTN24",
    # "Rodrigo_Rivera",
    # "bravorubendario",
    # "jcgalindovacha",
    # "TimoFARC",
    # "Carlozada_FARC",
    # "SandraFARC",
    "AlapePastorFARC"
]

for user in users:
    print(user)
    for tweet in t.GetUserTimeline(screen_name=user, count=200):
        q = urllib.parse.urlencode({"q": "to:%s" % user})
        try:
            replies = t.GetSearch(raw_query=q, since_id=tweet.id, max_id=None, count=10)
        except twitter.error.TwitterError as e:
            print("caught twitter api error"+str(e))
            time.sleep(60)
            continue
        for reply in replies:
            data_reply = {}
            data_reply["reply_id"] = reply.id
            data_reply["reply_text"] = reply.text
            data_reply["reply_username"] = reply.user.screen_name
            data_reply["reply_location"] = reply.user.location

            data_reply["original_id"] = tweet.id
            data_reply["original_username"] = tweet.user.screen_name
            data_reply["original_text"] = tweet.text
            data_reply["original_location"] = tweet.user.location
            result = db.replies.insert_one(data_reply)
