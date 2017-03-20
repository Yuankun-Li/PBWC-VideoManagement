from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

import django.contrib.auth.views
from videomanagement import views as video_views

from django.contrib import admin
admin.autodiscover()
from django.contrib.admindocs import urls as adminurls

urlpatterns = [
	# Only for test purpose
	# Home url need to be changed to home
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^$', video_views.community_retrieve, name='community_retrieve'),
	url(r'^login$', video_views.login_, name='login'),
	url(r'^logout$', video_views.logout_, name='logout'),
	url(r'^upload$', video_views.upload, name='upload'),
	url(r'^delete_video/(?P<video_id>\d+)/$', video_views.delete_video, name='delete_video'),
	url(r'^view_video/(?P<video_id>\d+)/$', video_views.view_video, name='view_video'),
	url(r'^get_video/(?P<video_id>\d+)/$', video_views.get_video, name='get_video'),
	url(r'^committee_videos$', video_views.committee_retrieve, name='committee_retrieve')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
