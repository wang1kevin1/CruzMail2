from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^$', views.account, name='account'),
	url(r'^login', auth_views.login,{'template_name': 'login.html'}, name='login'),
	url(r'^create', views.create, name='create'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^new_employee', views.new_employee, name='new_employee'),
	url(r'^update_user_bio', views.update_user_bio, name='update_user_bio'),
	url(r'^update_user_email', views.update_user_email, name='update_user_email'),
	url(r'^update_user_account_privacy', views.update_user_account_privacy, name='update_user_account_privacy'),
	url(r'^update_user_password', views.update_user_password, name='update_user_password'),
	url(r'^reset_password', views.reset_password, name='reset_password'),
]
