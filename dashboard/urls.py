from django.conf.urls import url

from .views import (
    IndexView,
    summary, accounts, hashtags, locations, quotes, polarities, topics, tweets,
    classify_tweet, accounts_classified, accounts_classified_summary
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^summary/$', summary, name='summary'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^accounts_classified/$', accounts_classified, name='accounts_classified'),
    url(r'^accounts_classified_summary/$', accounts_classified_summary, name='accounts_classified_summary'),
    url(r'^hashtags/$', hashtags, name='hashtags'),
    url(r'^locations/$', locations, name='locations'),
    url(r'^quotes/$', quotes, name='quotes'),
    url(r'^topics/$', topics, name='topics'),
    url(r'^polarities/$', polarities, name='polarities'),
    url(r'^tweets/$', tweets, name='tweets'),
    url(r'^classify_tweet/$', classify_tweet, name='classify_tweet'),
]
