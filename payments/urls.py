from django.conf.urls import url, include
from payments import views

urlpatterns = [
	url(r'^get_active_events/?',views.get_active_events,name='get_active_events'),

]