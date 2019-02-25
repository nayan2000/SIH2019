from django.conf.urls import url, include
from payments import views

urlpatterns = [
	url(r'^get_all_events/?',views.get_all_events,name='get_all_events'),

]