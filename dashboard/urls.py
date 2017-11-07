from django.conf.urls import url

from .views import (
    IndexView,
    tuits,
)


urlpatterns = [
    url(
        r'^$',
        IndexView.as_view(),
        name='index'
    ),
    url(
        r'^tuits/$',
        tuits,
        name='tuits'
    ),
]
