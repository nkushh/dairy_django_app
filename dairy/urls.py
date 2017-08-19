from django.conf.urls import url

from . import views

app_name = 'dairy'

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^cattle/$', views.fetch_cattle, name='cattle-list'),
	url(r'^add-cattle/$', views.add_cattle, name='add-cattle'),
	url(r'^new-cattle/$', views.new_cattle, name='new-cattle'),
	url(r'^cattle-detail/(?P<cattle_id>\d+)/$', views.cattle_detail, name='cattle-detail'),
	url(r'^edit-cattle/(?P<cattle_id>\d+)/$', views.edit_cattle, name='edit-cattle'),
	url(r'^update-cattle/(?P<cattle_id>\d+)/$', views.update_cattle, name='update-cattle'),
	url(r'^delete-cattle/(?P<cattle_id>\d+)/$', views.delete_cattle, name='delete-cattle'),
	url(r'^add-milk/$', views.add_milk, name='add-milk'),
	url(r'^milk-records/$', views.milk_records, name='milk-records'),
	url(r'^record-milk/$', views.record_milk_produced, name='record-milk'),
	url(r'^record-cattle-milk/$', views.record_cattle_milk, name='record-cattle-milk'),
	url(r'^monthly-milk-records/(\w+)/$', views.monthly_milk_records, name='monthly-records'),
	url(r'^milk-sale-records/$', views.milk_sale_records, name='milk-sale-records'),
	url(r'^record-milk-sale/$', views.record_milk_sale, name='record-milk-sale'),
	url(r'^monthly-milk-sales/(\w+)/$', views.monthly_milk_sales, name='monthly-sales'),
]