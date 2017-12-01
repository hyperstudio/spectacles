from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.documents),
    url(r'^documents$', views.documents),
    url(r'^documents$', views.documents),
    url(r'^documents/(\d+)$', views.document),

    url(r'^api/token$', views.api_token),
]

