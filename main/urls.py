from django.conf.urls import url
from django.contrib.auth.views import logout
from main import views
app_name = 'main'

urlpatterns = [
	url(r'^register/?',views.register,name='register'),
]