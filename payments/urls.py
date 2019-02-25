from django.conf.urls import url, include
from payments import views

urlpatterns = [
	url(r'^get_active_events/?',views.get_active_events,name='get_active_events'),
	url(r'^get_event_details/(?P<event_id>\d+)/?$', views.get_event_details, name='get_event_details'),

]