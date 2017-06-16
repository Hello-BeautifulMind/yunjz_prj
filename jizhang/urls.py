from django.conf.urls import url
from django.contrib import admin
from jizhang import views

admin.autodiscover()


urlpatterns = [
	# items
	url(r'^$', views.items, name='items'),
	url(r'^new/$', views.new_item, name='new_item'),
	url(r'^edit/(?P<item_id>\d+)/$', views.edit_item, name='edit_item'),
	url(r'^find/$', views.find_items, name='find_items'),
	url(r'^categories/$', views.categories, name='categories'),
	url(r'^categories/find/$', views.find_categories, name='find_categories'),
	url(r'^categories/new/$', views.new_category, name='new_category'),
	url(r'^categoryies/edit/(?P<c_id>\d+)/$', views.edit_category, name='edit_category'),
	# export excel
	url(r'^export/$', views.export_excel, name='export_excel'),
]


