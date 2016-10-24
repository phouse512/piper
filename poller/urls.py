from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^event/(?P<poll_id>\w{0,50})/save/(?P<answer_id>\w{0,50})/', views.save_vote, name='save'),
    url(r'^event/(?P<poll_id>\w{0,50})/', views.view_poll, name='view_poll'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^create_user/', views.create_user, name='create'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^', views.home, name='home')
]
