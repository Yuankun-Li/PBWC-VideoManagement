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
	url(r'^create_request/(?P<video_id>\d+)/$', video_views.create_request, name='create_request'),
	url(r'^retrieve_requests$', video_views.retrieve_requests, name='retrieve_requests'),
	url(r'^delete_request/(?P<request_id>\d+)/$', video_views.delete_request, name='delete_request'),
	url(r'^accept_request/(?P<request_id>\d+)/$', video_views.accept_request, name='accept_request'),
	url(r'^create_meeting_request$', video_views.create_meeting_request, name='create_meeting_request'),
	url(r'^retrieve_meeting_requests', video_views.retrieve_meeting_requests, name='retrieve_meeting_requests'),
	url(r'^delete_meeting_request/(?P<id>\d+)/', video_views.delete_meeting_request, name='delete_meeting_request'),
	url(r'^accept_meeting_request/(?P<id>\d+)/', video_views.accept_meeting_request, name='accept_meeting_request'),
	url(r'^committee_videos$', video_views.committee_retrieve, name='committee_retrieve'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
