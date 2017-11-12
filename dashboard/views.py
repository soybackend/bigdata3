# coding: utf-8
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from pymongo import MongoClient
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .classify_tweets import Classification


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
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['accounts'].find({}).skip(int(offset)).limit(int(limit))
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'id': dto['id'],
                'name': dto['name'],
                'username': dto['username'],
                'location': dto['location'],
                'image': dto['image'],
                'description': dto['description'],
                'tweets_count': dto['tweets_count'],
                'rtweets_count': dto['rtweets_count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def accounts_classified(request):
    data = db['account_classified'].find({})
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'account': dto['account'],
            'type': dto['type'],
            'topics': dto['topics'],
            'polarities': dto['polarities'],
            'polarity_score': dto['polarity_score'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def accounts_classified_summary(request):
    data = db['account_classified'].aggregate([{ '$group': { '_id' : '$type', 'count' : { '$sum' : 1} } }])
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'type': dto['_id'],
            'count': dto['count'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def hashtags(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['hashtags'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'hashtag': dto['hashtag'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def locations(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['locations'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'location': dto['location'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def quotes(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['quotes'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'quote': dto['quote'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def topics(request):
    data = db['topics'].find({}).sort('topic_id', 1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'topic_id': dto['topic_id'],
            'topic': dto['topic'],
            'count': dto['count'],
            'polarities' : dto['polarities'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def polarities(request):
    data = db['polarities'].find({}).sort('polarity_id', 1)
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
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['tweets'].find({}).skip(int(offset)).limit(int(limit))
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
                'topic' : dto['topic_name'],
                'polarity_id': dto['polarity_id'],
                'polarity': dto['polarity'],
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

@csrf_exempt
def classify_tweet(request):
    if request.method == 'POST':
        classifier = Classification()
        json_data = json.loads(request.body.decode('utf-8'))

        # create dataset
        dataset = classifier.generate_dataset_single_text(json_data['text'])
        # Classify tweets by topic
        clf_topics = classifier.classify_by_topic(dataset)
        topic_id = int(clf_topics[0])
        # Classify tweets by polarity
        clf_polarities = classifier.classify_by_polarity(dataset)
        polarity_id = int(clf_polarities[0])

        result = {
            'text': json_data['text'],
            'topic_id': topic_id,
            'topic' : get_topic(topic_id),
            'polarity_id': polarity_id,
            'polarity': get_polarity(polarity_id),
        }
    else:
        result = "Method incorrect"
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")
