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

    # get the first worksheet
    sheet = book.sheet_by_index(1)

    for col in range(1, 7):

        for index in range(1, sheet.nrows):
            cells = sheet.row_slice(rowx=index,
                                    start_colx=0,
                                    end_colx=11)
            rating_col = 4 + col
            polarity_id = sheet.cell(index, rating_col).value

            if polarity_id != '':
                polarity = 'other'
                if polarity_id == 1:
                    polarity = 'negative'
                    polarity_id = 1
                elif polarity_id == 2:
                    polarity = 'positive'
                    polarity_id = 2
                elif polarity_id == 3:
                    polarity = 'mixed'
                    polarity_id = 3
                elif polarity_id == 4:
                    polarity = 'other'
                    polarity_id = 4

                data = {
                    "id" : sheet.cell(index, 0).value,
                    "date" : sheet.cell(index, 1).value,
                    "account_name" : sheet.cell(index, 3).value,
                    "account_nickname" : sheet.cell(index, 4).value,
                    "text" : sheet.cell(index, 2).value,
                    "polarity_id" : polarity_id,
                    "polarity" : polarity,
                }
                # db.tweets_classified_dataset_english.insert_one(data)

if __name__ == "__main__":
    path = "/Users/farruza/Downloads/dataset_anotado.xlsx"
    load_file(path)
