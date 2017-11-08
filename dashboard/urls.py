from django.conf.urls import url

from .views import (
    IndexView,
    summary, accounts, hashtags, locations, quotes,
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^summary/$', summary, name='summary'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(r'^hashtags/$', hashtags, name='hashtags'),
    url(r'^locations/$', locations, name='locations'),
    url(r'^quotes/$', quotes, name='quotes'),
]
