from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<group_hash>\w{0,50})/track/(?P<event_id>\w{0,50})/save/', views.save, name='save'),
    url(r'^(?P<group_hash>\w{0,50})/track/(?P<event_id>\w{0,50})/toggle/', views.event_toggle, name='toggle'),
    url(r'^(?P<group_hash>\w{0,50})/track/(?P<event_id>\w{0,50})/', views.tracking, name='track'),
    url(r'^(?P<group_hash>\w{0,50})/_search/', views.search, name='search'),
    url(r'^(?P<group_hash>\w{0,50})/admin/', views.admin_overview, name='admin')
]
