from django.conf.urls import url

from .views import (
    IndexView, TweetsView, PolaritiesView, AccountsView, HastagsView,
    summary, accounts, hashtags, locations, quotes, polarities, topics, tweets,
    classify_tweet, accounts_classified, accounts_classified_summary,
    LocationsView, QuotesView, TopicsView, TagCloudView, ClassifyView,
    AccountsTypeView, selected_accounts, MainAccountsView, MainAccountsDetailView
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^summary/$', summary, name='summary'),
    url(r'^accounts/$', accounts, name='accounts'),
    url(
        r'^accounts_classified/$',
        accounts_classified,
        name='accounts_classified'
    ),
    url(
        r'^accounts_classified_summary/$',
        accounts_classified_summary,
        name='accounts_classified_summary'
    ),
    url(r'^hashtags/$', hashtags, name='hashtags'),
    url(r'^locations/$', locations, name='locations'),
    url(r'^quotes/$', quotes, name='quotes'),
    url(r'^topics/$', topics, name='topics'),
    url(r'^polarities/$', polarities, name='polarities'),
    url(r'^tweets/$', tweets, name='tweets'),
    url(r'^ver-tweets/$', TweetsView.as_view(), name='tweets-view'),
    url(r'^classify_tweet/$', classify_tweet, name='classify_tweet'),
    url(r'^selected_accounts/$', selected_accounts, name='selected_accounts'),
    url(
        r'^ver-polaridades/$',
        PolaritiesView.as_view(),
        name='polarities-view'
    ),
    url(
        r'^ver-cuentas-involucradas/$',
        AccountsView.as_view(),
        name='accounts-view'
    ),
    url(
        r'^ver-hastags/$',
        HastagsView.as_view(),
        name='hashtags-view'
    ),
    url(
        r'^ver-ubicaciones/$',
        LocationsView.as_view(),
        name='locations-view'
    ),
    url(
        r'^ver-citas/$',
        QuotesView.as_view(),
        name='quotes-view'
    ),
    url(
        r'^ver-topicos/$',
        TopicsView.as_view(),
        name='topics-view'
    ),
    url(
        r'^tagcloud/$',
        TagCloudView.as_view(),
        name='tagcloud-view'
    ),
    url(
        r'^clasificar/$',
        ClassifyView.as_view(),
        name='classify-view'
    ),
    url(
        r'^cuentas-tipo/$',
        AccountsTypeView.as_view(),
        name='accounts-type-view'
    ),
    url(
        r'^cuentas-principales/$',
        MainAccountsView.as_view(),
        name='main-accounts-view'
    ),
    url(
        r'^cuentas-principales/(?P<scree_name>[\w-]+)$',
        MainAccountsDetailView.as_view(),
        name='main-accounts-detail-view'
    ),
]
