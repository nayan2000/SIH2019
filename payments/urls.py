from django.conf.urls import url, include
from payments import views

app_name = 'payments'

urlpatterns = [
	# to get active events
	url(r'^get_active_events/?',views.get_active_events,name='get_active_events'),

	# to get details of a particular event
	url(r'^get_event_details/(?P<event_id>\d+)/?$', views.get_event_details, name='get_event_details'),

	# to send a payment request
	url(r'^payment_request/?',views.payment_request,name='payment_request'),

	#callback url for instamojo
	url(r'^payment_response/?$',views.payment_response,name='payment_response'),

	#to add event through web portal
	url(r'^add_event/?',views.add_event,name='add_event'),

]