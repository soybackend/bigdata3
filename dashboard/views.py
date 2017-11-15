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
        data = db['accounts'].find({}).skip(int(offset)).limit(int(limit)).sort([('tweets_count', -1)])
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

def selected_accounts(request):
    data = db['accounts_selected_trace'].aggregate([{ '$group': {
                                                   '_id': { 'screen_name': '$screen_name',
                                                   'name': '$name',
                                                   'image': '$image',
                                                   'description': '$description'}

    }}])
    result = []
    for dto in data:
        print(dto)
        json_data = {
            'screen_name': dto['_id']['screen_name'],
            'name': dto['_id']['name'],
            'image': dto['_id']['image'],
            'description': dto['_id']['description'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def accounts_classified(request):
    sort = request.GET.get('sort')
    username = request.GET.get('username')
    if username is not None:
        data = db['account_classified'].find({'account' : username})
    else:
        sort = request.GET.get('sort')
        if sort is None or sort not in ['1','-1']:
            sort = -1
        data = db['account_classified'].find({}).sort('polarity_score', int(sort))

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
    topic = 'sin clasificar'
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
    polarity = 'sin clasificar'
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

def get_polarity_english(key):
    polarity = 'not classified'
    if key == 1:
        polarity = 'negative'
    elif key == 2:
        polarity = 'positive'
    elif key == 3:
        polarity = 'mixed'
    elif key == 4:
        polarity = 'other'
    return polarity


class TweetsView(TemplateView):
    template_name = 'dashboard/tweets.html'

    def get_context_data(self, **kwargs):
        context = super(TweetsView, self).get_context_data(**kwargs)
        context['tweets'] = db['tweets'].find({}).limit(5000)
        return context


@csrf_exempt
def classify_tweet(request):
    lang = request.GET.get('lang')

    if request.method == 'POST':
        classifier = Classification()
        json_data = json.loads(request.body.decode('utf-8'))

        if lang is None or lang == 'es':
            # create dataset
            dataset = classifier.generate_dataset_single_text('spanish', json_data['text'])
            # Classify tweets by topic
            clf_topics = classifier.classify_by_topic(dataset)
            topic_id = int(clf_topics[0])
            # Classify tweets by polarity
            clf_polarities = classifier.classify_by_polarity(dataset)
            polarity_id = int(clf_polarities[0])
            polarity = get_polarity(polarity_id)
        else :
            # create dataset
            dataset = classifier.generate_dataset_single_text('english', json_data['text'])
            topic_id = 0
            # Classify tweets by polarity
            clf_polarities = classifier.classify_by_polarity_english(dataset)
            polarity_id = int(clf_polarities[0])
            polarity = get_polarity_english(polarity_id)

        result = {
            'text': json_data['text'],
            'topic_id': topic_id,
            'topic' : get_topic(topic_id),
            'polarity_id': polarity_id,
            'polarity': polarity,
        }
    else:
        result = "Method incorrect"
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

class PolaritiesView(TemplateView):
    template_name = 'dashboard/polaridades.html'


class AccountsView(TemplateView):
    template_name = 'dashboard/cuentas.html'


class HastagsView(TemplateView):
    template_name = 'dashboard/hastags.html'

    def get_context_data(self, **kwargs):
        context = super(HastagsView, self).get_context_data(**kwargs)
        context['hashtags'] = db['hashtags'].find({})
        return context


class LocationsView(TemplateView):
    template_name = 'dashboard/locations.html'

    def get_context_data(self, **kwargs):
        context = super(LocationsView, self).get_context_data(**kwargs)
        context['locations'] = db['locations'].find({}).sort('count', -1)
        return context


class QuotesView(TemplateView):
    template_name = 'dashboard/quotes.html'

    def get_context_data(self, **kwargs):
        context = super(QuotesView, self).get_context_data(**kwargs)
        context['quotes'] = db['quotes'].find({}).sort('count', -1)
        return context


class TopicsView(TemplateView):
    template_name = 'dashboard/topics.html'


class TagCloudView(TemplateView):
    template_name = 'dashboard/tagcloud.html'


class ClassifyView(TemplateView):
    template_name = 'dashboard/clasify.html'


class AccountsTypeView(TemplateView):
    template_name = 'dashboard/accounts-type.html'


class MainAccountsView(TemplateView):
    template_name = 'dashboard/cuentas-principales.html'
