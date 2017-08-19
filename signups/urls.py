from django.conf.urls import url

from . import views

app_name = 'signups'

urlpatterns = [
	url(r'^$', views.home, name="signup"),
]