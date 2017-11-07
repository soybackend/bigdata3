from django.shortcuts import render
from django.views.generic import TemplateView
from pymongo import MongoClient
from django.http import JsonResponse

client = MongoClient('localhost', 27017)
db = client['twitter']
tuits_collection = db['tuits']


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'


def tuits(request):
    data = tuits_collection.find({}).count()
    return JsonResponse(data, safe=False)
