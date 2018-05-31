# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import url, include
from django.contrib import admin
import spectacles.views
import spectacles.views.auth
import spectacles.views.api
import spectacles.views.datastore


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # spectacles routes
    url(r'^$', spectacles.views.index, name='spectacles-root'),
    url(r'^archive$', spectacles.views.archive, name='spectacles-archive'),
    url(r'^documents$', spectacles.views.archive, name='spectacles-archive'),
    url(r'^documents/(\d+)$', spectacles.views.document, name='spectacles-document'),
    ### Authentication
    url(r'^auth/register$', spectacles.views.auth.register, name='auth-register'),
    url(r'^auth/login$', spectacles.views.auth.login, name='auth-login'),
    url(r'^auth/logout$', spectacles.views.auth.logout, name='auth-logout'),

    # API
    url(r'^api/search$', spectacles.views.api.search_annotations, name='api-search'),
    url(r'^activity$', spectacles.views.user, name='api-user'),
    url(r'^activity/(?P<user_id>\d+)$', spectacles.views.user, name='api-user'),
    url(r'^api/search/annotations$', spectacles.views.api.search_annotations, name='api-search-anns'),
    url(r'^api/search/documents$', spectacles.views.api.search_documents, name='api-search-docs'),
    url(r'^api/similar/annotation/(?P<annotation_id>[0-9a-f-]+)$', spectacles.views.api.similar_annotations, name='api-sim-anns'),
    #url(r'^api/documents/(?P<document_id>\d+)$', views.api_document, name='api-document'),
    #url(r'^api/annotations$', views.api_annotations, name='api-annotations'),
    #url(r'^api/annotations/(?P<annotation_id>[0-9a-f-]+)$', views.api_annotation, name='api-annotation'),
    url(r'^api/bookmark$', spectacles.views.api.bookmark_crud, name='api-bookmark-crud'),
    url(r'^api/bookmark/(?P<bookmark_id>\d+)$', spectacles.views.api.bookmark_crud, name='api-bookmark-crud'),
    ### Datastore
    url(r'^api/store/token$', spectacles.views.datastore.token, name='ds-token'),
    url(r'^api/store/(?P<document_id>\d+)$',
        spectacles.views.datastore.crud,
        name='ds-store-crud'),
    url(r'^api/store/(?P<document_id>\d+)/(?P<annotation_id>[0-9a-f-]+)$',
        spectacles.views.datastore.crud,
        name='ds-store-crud'),
]
