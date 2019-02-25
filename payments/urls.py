from django.conf.urls import url, include
from payments import views

app_name = 'payments'

urlpatterns = [
	url(r'^get_active_events/?',views.get_active_events,name='get_active_events'),
	url(r'^get_event_details/(?P<event_id>\d+)/?$', views.get_event_details, name='get_event_details'),
	url(r'^payment_request/?',views.payment_request,name='payment_request'),
	url(r'^payment_response/?$',views.payment_response,name='payment_response'),

]