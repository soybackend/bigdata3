import os
import twitter

api = twitter.Api(consumer_key=os.environ['consumer_key'],
                  consumer_secret=os.environ['consumer_secret'],
                  access_token_key=os.environ['access_token'],
                  access_token_secret=os.environ['access_token_secret'])


tuit = api.GetStatus(928369222656430080)
print(tuit)
