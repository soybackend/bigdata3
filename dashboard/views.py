from django.shortcuts import render
from django.views.generic import TemplateView
from pymongo import MongoClient
from django.http import JsonResponse

client = MongoClient('localhost', 27017)
db = client['twitter']

class IndexView(TemplateView):
    template_name = 'dashboard/index.html'


def summary(request):
    data = db['summary'].find_one({})
    # print(data)
    json_data = {
        'total_tweets': data['total_tweets'],
        'total_rts': data['total_rts'],
        'total_accounts': data['total_accounts'],
        'total_hashtags': data['total_hashtags'],
        'total_quotes': data['total_quotes']
    }
    return JsonResponse(json_data, safe=False)

def accounts(request):
    data = db['accounts'].find({})
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'id': dto['id'],
            'name': dto['name'],
            'username': dto['username'],
            'location': dto['location'],
            'description': dto['description'],
            'tweets_count': dto['tweets_count']
        }
        result.append(json_data)
    return JsonResponse(result, safe=False)

def hashtags(request):
    data = db['hashtags'].find({}).sort('count', -1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'hashtag': dto['hashtag'],
            'count': dto['count'],
        }
        result.append(json_data)
    return JsonResponse(result, safe=False)

def locations(request):
    data = db['locations'].find({}).sort('count', -1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'location': dto['location'],
            'count': dto['count'],
        }
        result.append(json_data)
    return JsonResponse(result, safe=False)

def quotes(request):
    data = db['quotes'].find({}).sort('count', -1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'quote': dto['quote'],
            'count': dto['count'],
        }
        result.append(json_data)
    return JsonResponse(result, safe=False)
