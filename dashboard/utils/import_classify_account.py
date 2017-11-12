# coding: utf-8
from pymongo import MongoClient
import xlrd
import numpy

def get_topic(key):
    topic = 'Sin clasificar'
    if key == 0:
        topic = 'otro'
    elif key == 1:
        topic = 'proceso de paz'
    elif key == 2:
        topic = 'electoral'
    elif key == 3:
        topic = 'corrupción'
    return topic

def get_polarity(key):
    polarity = 'Sin clasificar'
    if key == 1:
        polarity = 'negativo'
    elif key == 2:
        polarity = 'casi negativo'
    elif key == 3:
        polarity = 'neutro'
    elif key == 4:
        polarity = 'casi positivo'
    elif key == 5:
        polarity = 'positivo'
    return polarity

def load_file(path):

    client = MongoClient('localhost', 27017)
    db = client.twitter
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)

    # print number of sheets
    # print (book.nsheets)

    # print sheet names
    # print (book.sheet_names())

    # get the first worksheet
    sheet = book.sheet_by_index(0)

    for index in range(1, sheet.nrows):
        cells = sheet.row_slice(rowx=index,
                                start_colx=0,
                                end_colx=2)
        account = sheet.cell(index, 0).value

        # Add topics info
        rs = db.tweets.aggregate([{ '$match': { 'tweet.user.screen_name' : account }},
                                 { '$group': { '_id' : "$topic_id", 'count':{ '$sum' : 1} } }])
        topics = []
        for r in rs:
            tp = { "topic_id" : r['_id'],
                   "topic" : get_topic(r['_id']),
                   "count" : r['count']
                 }
            topics.append(tp)

        # Add polarity info
        polarity_score = 3
        polarity_accumulate = 0
        polarity_count = 0
        rs_p = db.tweets.aggregate([{ '$match': { 'tweet.user.screen_name' : account }},
                                 { '$group': { '_id' : "$polarity_id", 'count':{ '$sum' : 1} } }])
        polarities = []
        for r in rs_p:
            pt = { "polarity_id" : r['_id'],
                   "polarity" : get_polarity(r['_id']),
                   "count" : r['count']
                 }
            polarity_accumulate = polarity_accumulate + int(r['_id']) * int(r['count'])
            polarity_count = polarity_count + int(r['count'])
            polarities.append(pt)

        if polarity_accumulate != 0:
            polarity_score = float(polarity_accumulate) / float(polarity_count)
        polarity_score = str(numpy.around([polarity_score], 2)[0])

        data = {
            "account" : account,
            "type" : sheet.cell(index, 2).value,
            "topics" : topics,
            "polarities" : polarities,
            'polarity_score' : float(polarity_score),
        }
        # print(data)
        db.account_classified.insert_one(data)

if __name__ == "__main__":
    path = "/Users/farruza/Downloads/Clasif-Cuentas_Twitter.xlsx"
    load_file(path)
