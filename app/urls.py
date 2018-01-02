from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.documents, name='app-root'),
    url(r'^documents$', views.documents, name='app-documents'),
    url(r'^documents/(\d+)$', views.document, name='app-document'),

    url(r'^auth/login$', views.login, name='app-login'),
    url(r'^auth/logout$', views.logout, name='app-logout'),

    url(r'^api/token$', views.api_token, name='api-token'),

    url(r'^api/store/(?P<document_id>\d+)$',
        views.api_store_crud,
        name='api-store-crud'),
    url(r'^api/store/(?P<document_id>\d+)/(?P<annotation_id>[0-9a-f-]+)$',
        views.api_store_crud,
        name='api-store-crud'),

    url(r'^api/search/documents$', views.api_search_documents, name='api-search-documents'),
    url(r'^api/search/annotations$', views.api_search_annotations, name='api-search-annotations'),

    #url(r'^api/documents/(?P<document_id>\d+)$', views.api_document, name='api-document'),
    #url(r'^api/annotations$', views.api_annotations, name='api-annotations'),
    #url(r'^api/annotations/(?P<annotation_id>[0-9a-f-]+)$', views.api_annotation, name='api-annotation'),
]

