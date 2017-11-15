from __future__ import print_function
import twitter

CONSUMER_KEY = 'rnSCGSqg7IdytdFz7pL5lGNDj'
CONSUMER_SECRET = 'MzYwxrshahZSEWibNGO4cXa25lgyUKbVFEd1XvpkFkB0PVizgv'
ACCESS_TOKEN = '312397870-aOWVDkctz4KW7uyRPaw2KNx5lbHjWloIAMg4dBDw'
ACCESS_TOKEN_SECRET = 'VPjLb6yuaL39JCYdniTcVYP1kgSbCBHBcnfZ7K50e2Jb7'


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

users = api.GetFollowers(screen_name='farruza', total_count=100)

print([u.screen_name for u in users])
