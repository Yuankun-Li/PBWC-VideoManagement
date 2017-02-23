from django.conf.urls import url
from django.contrib.auth import views as auth_views

from videomanagement import views as video_views

urlpatterns = [
	# Only for test purpose
	# Home url need to be changed to home
	url(r'^$', video_views.upload, name='upload'),
	url(r'^upload$', video_views.upload, name='upload'),
]