from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^connect/', views.connect, name='connect'),
    url(r'^job/', views.github_job, name='github_job'),
    url(r'^tail/', views.commit_tail, name='commit_tail')
]