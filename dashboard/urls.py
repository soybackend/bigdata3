from django.conf.urls import url

from .views import (
    IndexView,
    summary, accounts, hashtags, locations, quotes, polarities, topics, tweets
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^summary/$', summary, name='summary'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^hashtags/$', hashtags, name='hashtags'),
    url(r'^locations/$', locations, name='locations'),
    url(r'^quotes/$', quotes, name='quotes'),
    url(r'^topics/$', topics, name='topics'),
    url(r'^polarities/$', polarities, name='polarities'),
    url(r'^tweets/$', tweets, name='tweets'),
]
