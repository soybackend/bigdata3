# coding: utf-8
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.twitter

    accounts = db.accounts_selected_trace.find({ 'image': { '$exists': True } })

    for ac in accounts:
        nvars = {
            "image" : ac['image'],
        }
        db.accounts_selected_trace.update( {'screen_name' : ac['screen_name'], 'image': { '$exists': False }}, {'$set' : nvars} )
