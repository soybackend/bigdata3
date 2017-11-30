from __future__ import print_function
import twitter
from twitter.error import TwitterError
import json
from pymongo import MongoClient

CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_TOKEN_SECRET = 'xxxx'


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

client = MongoClient('localhost', 27017)
db = client.twitter

accounts = db.recolected_followers.find({})

for account in accounts:
    content = json.loads(account['follower'])
    try:
        profile = api.GetUser(screen_name=content['screen_name'])
        print(content['screen_name'])
        # if int(profile.statuses_count) > 500000:
        print(profile.friends_count)
        print(profile.followers_count)
        print(profile.statuses_count)
        if int(profile.friends_count) == 2001 or int(profile.followers_count) == 0 or int(profile.statuses_count) > 1000000:
            descrip = 'Cantidad de tweets ' + str(profile.statuses_count) + ', '
            descrip = descrip + 'siguiendo a ' + str(profile.friends_count)
            descrip = descrip + ' cuentas y con ' + str(profile.followers_count)
            descrip = descrip + ' seguidores'
            data = {
                "account_name" : content['screen_name'],
                "image" : profile.profile_image_url,
                "description" : descrip,
                "friends_count" : profile.friends_count,
                "followers_count" : profile.followers_count,
                "statuses_count " : profile.statuses_count,
            }
            print(profile)
            db.accounts_robot.insert_one(data)
        try:
            db.recolected_followers.delete_one({ '_id' : account['_id'] })
        except:
            pass
    except twitter.TwitterError as error:
        print('error: ' + str(error.message))

#    print(account)
# users = api.GetFollowers(screen_name=accounts[0], total_count=100)
# print([u.screen_name for u in users])
