from __future__ import print_function
import twitter

CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_TOKEN_SECRET = 'xxxx'


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

users = api.GetFollowers(screen_name='farruza', total_count=100)

print([u.screen_name for u in users])
