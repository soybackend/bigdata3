import twitter, time, json, logging
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter']

with open('config.json') as data_file:
    json_config = json.load(data_file)

api = twitter.Api(consumer_key=json_config['twitter']['consumer_key'],
                      consumer_secret=json_config['twitter']['consumer_secret'],
                      access_token_key=json_config['twitter']['access_token_key'],
                      access_token_secret=json_config['twitter']['access_token_secret'],
                      sleep_on_rate_limit=True)

def writeFollowersToFile(followers, username):
    print(username)
    for friend in followers:
        user = api.GetUser(user_id=friend).AsJsonString()
        db.followers.insert_one({"user": username, "follower": user})

friends = []
for name in json_config['accounts']:
    print(name)
    friends = api.GetFollowerIDs(screen_name=name)
    writeFollowersToFile(friends, name)
