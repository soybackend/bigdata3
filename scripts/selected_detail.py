import os
import twitter
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter']

api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")


accounts = [
    "JuanLozano_R",
    "RafaelPardo",
    "ernestosamperp",
    "AndresPastrana_",
    "RestrepoJCamilo",
    "CristoBustos",
    "HoracioSerpa",
    "alejogiral",
    "Rodrigo_Lara_",
    "carlosfgalan",
    "AABenedetti",
    "JuanManSantos",
    "CGurisattiNTN24",
    "Rodrigo_Rivera",
    "bravorubendario",
    "jcgalindovacha",
    "TimoFARC",
    "Carlozada_FARC",
    "SandraFARC",
    "AlapePastorFARC"
]

for account in accounts:
    try:
        user = api.GetUser(screen_name=account)
        print(user)
        data_user = {}
        data_user['created_at'] = user.created_at
        data_user['description'] = user.description
        data_user['favourites_count'] = user.favourites_count
        data_user['followers_count'] = user.followers_count
        data_user['friends_count'] = user.friends_count
        data_user['name'] = user.name
        data_user['screen_name'] = user.screen_name
        data_user['image'] = user.profile_image_url
        result = db.accounts_selected_trace.insert_one(data_user)
    except:
        pass
