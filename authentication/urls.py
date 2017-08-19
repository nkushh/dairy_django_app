from django.conf.urls import url
from . import views


app_name = 'authentication'
urlpatterns = [
	url(r'^accounts/$', views.all_accounts, name='accounts'),
	url(r'^register-user/$', views.register_user, name='register_user'),
]