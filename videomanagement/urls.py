from django.conf.urls import url
from django.contrib.auth import views as auth_views

import django.contrib.auth.views
from videomanagement import views as video_views

urlpatterns = [
	# Only for test purpose
	# Home url need to be changed to home
	url(r'^$', video_views.upload, name='upload'),
	url(r'^login$', video_views.login_, name='login'),
	url(r'^login_manager$', video_views.login_manager, name='login_manager'),
	url(r'^logout$', video_views.logout_, name='logout'),
	url(r'^upload$', video_views.upload, name='upload'),
]