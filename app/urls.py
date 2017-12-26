from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.documents, name='app-root'),
    url(r'^documents$', views.documents, name='app-docs'),
    url(r'^documents/(\d+)$', views.document, name='app-doc'),

    url(r'^auth/login$', views.login, name='app-login'),
    url(r'^auth/logout$', views.logout, name='app-logout'),

    url(r'^api/token$', views.api_token, name='api-token'),

    url(r'^api/store/(\d+)$',
        views.api_store_crud,
        name='api-store-crud'),
    url(r'^api/store/(\d+)/(\d+)$',
        views.api_store_crud,
        name='api-store-crud'),
    url(r'^api/store/(\d+)/search$',
        views.api_store_search,
        name='api-store-search'),
]

