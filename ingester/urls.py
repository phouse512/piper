from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^job/(?P<job_id>[0-9]+)/', views.job_trigger, name='job_trigger')
]