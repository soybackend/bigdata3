# coding: utf-8
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from pymongo import MongoClient
from django.http import HttpResponse


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
    return HttpResponse(json.dumps(json_data, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

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
            'tweets_count': dto['tweets_count'],
            'rtweets_count': dto['rtweets_count'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

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
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

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
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

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
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def topics(request):
    data = db['topics'].find({}).sort('count', -1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'topic_id': dto['topic_id'],
            'topic': dto['topic'],
            'count': dto['count'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def polarities(request):
    data = db['polarities'].find({}).sort('count', -1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'polarity_id': dto['polarity_id'],
            'polarity': dto['polarity'],
            'count': dto['count'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def tweets(request):
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))

    if (limit is not None and offset is not None):
        data = db['tweets'].find({}).skip(offset).limit(limit)
        result = []
        for dto in data:
            try:
                location = dto['location']['place']
            except:
                location = "Sin información"

            json_data = {
                'time': dto['tweet']['created_at'],
                'text': dto['tweet']['text'],
                'account': dto['tweet']['user']['screen_name'],
                'location': location,
                'topic_id': dto['topic_id'],
                'topic' : get_topic(dto['topic_id']),
                'polarity_id': dto['polarity_id'],
                'polarity': get_polarity(dto['polarity_id']),
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

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
