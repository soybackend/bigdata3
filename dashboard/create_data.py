# coding: utf-8
from pymongo import MongoClient
import re


def append_list_to_dict(dist, list):
    for x in list:
        if x in dist:
            dist[x] = dist[x] + 1
        else:
            dist[x] = 1

def append_value_to_dict(dist, value):
    if value in dist:
        dist[value] = dist[value] + 1
    else:
        dist[value] = 1

def append_user_to_dict(dist, tweet):
    user = tweet['user']
    user_id = user['id']
    if user_id not in dist:
        if tweet['text'].startswith('RT'):
            user['tweets_count'] = 0
            user['rtweets_count'] = 1
        else:
            user['tweets_count'] = 1
            user['rtweets_count'] = 0
    else:
        if tweet['text'].startswith('RT'):
            user['tweets_count'] = dist[user_id]['tweets_count']
            user['rtweets_count'] = dist[user_id]['rtweets_count'] + 1
        else:
            user['tweets_count'] = dist[user_id]['tweets_count'] + 1
            user['rtweets_count'] = dist[user_id]['rtweets_count']
    dist[user_id] = user
    loc = dist[user_id]['location']
    if loc is not None and len(loc) != 0:
        loc = loc.strip().lower()
        if 'colombia' in loc or 'bogotá' in loc or 'bogota' in loc:
            loc = 'Colombia'
        if '4.6' in loc and '-74.0' in loc:
            loc = 'Colombia'
        dist[user_id]['location'] = loc

def extract_field(prefix, text):
    rs = []
    text = text.replace('\n', ' ')
    while True:
        field_search = re.search(prefix + '([A-Za-z0-9ñÑáéíóúÁÉÍÓÚ]*)(.| )', text, re.IGNORECASE)
        if not field_search:
            break
        field = field_search.group(1)
        rs.append(prefix + field)
        text = text[text.index(prefix) + 1 : len(text)]

    try:
        field = text[text.index(prefix) + 1 : len(text)]
        rs.append(prefix + field)
    except ValueError:
        pass
    return rs

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    # Summary
    total_TW = db.tweets.count({})
    total_RT = db.tweets.count({'payload':{'$regex':'^RT'}})

    # Accounts
    tweets_accounts = db.tweets.find({}, {'tweet.user.id': 1, 'tweet.user.name': 1, 'tweet.user.screen_name': 1, 'tweet.user.location': 1, 'tweet.user.description': 1, 'tweet.text' : 1, '_id': 0})
    accounts = {}
    for account in tweets_accounts:
        append_user_to_dict(accounts, account['tweet'])
    # print(accounts)
    for key, value in accounts.items():
        data = {
            "id" : key,
            "name" : value['name'],
            "username" : value['screen_name'],
            "location" : value['location'],
            "description" : value['description'],
            "tweets_count" : value['tweets_count'],
            "rtweets_count" : value['rtweets_count'],
        }
        # db.accounts.insert_one(data)
    total_accounts = len(accounts)

    # Locations
    tweets_locations = db.tweets.find({}, {'location': 1, '_id': 0})
    locations = {}
    for location in tweets_locations:
        if len(location) != 0:
            loc = location['location']['place'].strip().lower()
            if 'colombia' in loc or 'bogotá' in loc or 'bogota' in loc:
                loc = 'Colombia'
            if '4.6' in loc and '-74.0' in loc:
                loc = 'Colombia'
        append_value_to_dict(locations, loc)
    #print(locations)
    for key, value in locations.items():
        data = {
            "location" : key,
            "count" : value,
        }
        # db.locations.insert_one(data)

    # Hashtags
    tweets_hashtags = db.tweets.find({'payload':{'$regex':'#'}})
    hashtags = {}
    for tweet_text in tweets_hashtags:
        append_list_to_dict(hashtags, extract_field('#', tweet_text['payload']))
    # print(hashtags)
    # print(len(hashtags))
    for key, value in hashtags.items():
        data = {
            "hashtag" : key,
            "count" : value,
        }
        # db.hashtags.insert_one(data)

    # Quotes
    tweets_qts = db.tweets.find( {'payload':{'$regex':'@'}} )
    qts = {}
    for tweet_text in tweets_qts:
         append_list_to_dict(qts, extract_field('@', tweet_text['payload']))
    # print(qts)
    # print(len(qts))
    for key, value in qts.items():
        data = {
            "quote" : key,
            "count" : value,
        }
        # db.quotes.insert_one(data)

    data = {
        "total_tweets" : total_TW,
        "total_rts" : total_RT,
        "total_accounts" : total_accounts,
        "total_hashtags" : len(hashtags),
        "total_quotes" : len(qts),
    }
    print(data)
    # dto_id = db.summary.insert_one(data).inserted_id
