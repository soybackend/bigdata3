# coding: utf-8
from pymongo import MongoClient
import xlrd

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
                                end_colx=5)
        topic = sheet.cell(index, 3).value
        topic_id = 0
        if topic == 'proceso de paz':
            topic_id = 1
        elif topic == 'electoral':
            topic_id = 2
        elif topic == 'corrupción':
            topic_id = 4

        polarity_id = sheet.cell(index, 4).value
        polarity = 'neutro'
        if polarity_id == 1:
            polarity = 'negativo'
        elif polarity_id == 2:
            polarity = 'casi negativo'
        elif polarity_id == 4:
            polarity = 'casi positivo'
        elif polarity_id == 5:
            polarity = 'positivo'

        data = {
            "id" : sheet.cell(index, 0).value,
            "account" : sheet.cell(index, 1).value,
            "text" : sheet.cell(index, 2).value,
            "topic_id" : topic_id,
            "topic" : topic,
            "polarity_id" : polarity_id,
            "polarity" : polarity,
        }
        db.tweets_classified.insert_one(data)

if __name__ == "__main__":
    path = "/Users/farruza/Downloads/ListadoTuits.xlsx"
    load_file(path)
