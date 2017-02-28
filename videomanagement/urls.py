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
	url(r'^$', video_views.upload, name='upload'),
	url(r'^login$', video_views.login_, name='login'),
	url(r'^login_manager$', video_views.login_manager, name='login_manager'),
	url(r'^community_main$', video_views.community_retrieve, name='community_retrieve'),
	url(r'^logout$', video_views.logout_, name='logout'),
	url(r'^upload$', video_views.upload, name='upload'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
