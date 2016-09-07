from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^track/', views.tracking, name='track'),
]
