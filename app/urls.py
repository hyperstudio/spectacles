# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import url

import app.views
import app.views.auth
import app.views.api
import datastore.views

urlpatterns = [
    # App routes
    url(r'^$', app.views.index, name='app-root'),
    url(r'^documents$', app.views.documents, name='app-documents'),
    url(r'^documents/(\d+)$', app.views.document, name='app-document'),
    ### Authentication
    url(r'^auth/login$', app.views.auth.login, name='auth-login'),
    url(r'^auth/logout$', app.views.auth.logout, name='auth-logout'),

    # API
    url(r'^api/search$', app.views.api.search_annotations, name='api-search'),
    url(r'^activity$', app.views.user, name='api-user'),
    url(r'^activity/(?P<user_id>\d+)$', app.views.user, name='api-user'),
    url(r'^api/search/annotations$', app.views.api.search_annotations, name='api-search-anns'),
    url(r'^api/search/documents$', app.views.api.search_documents, name='api-search-docs'),
    #url(r'^api/documents/(?P<document_id>\d+)$', views.api_document, name='api-document'),
    #url(r'^api/annotations$', views.api_annotations, name='api-annotations'),
    #url(r'^api/annotations/(?P<annotation_id>[0-9a-f-]+)$', views.api_annotation, name='api-annotation'),
    url(r'^api/bookmark$', app.views.api.bookmark_crud, name='api-bookmark-crud'),
    url(r'^api/bookmark/(?P<bookmark_id>\d+)$', app.views.api.bookmark_crud, name='api-bookmark-crud'),
    ### Datastore
    url(r'^api/store/token$', datastore.views.token, name='ds-token'),
    url(r'^api/store/(?P<document_id>\d+)$',
        datastore.views.crud,
        name='ds-store-crud'),
    url(r'^api/store/(?P<document_id>\d+)/(?P<annotation_id>[0-9a-f-]+)$',
        datastore.views.crud,
        name='ds-store-crud'),
]
