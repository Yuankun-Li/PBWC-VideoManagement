from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Video model: Include basic information about upload video information
# retention need to be modified in V2
# content_type need to be fixed

class Video(models.Model):
	"""
	Stores a single video entry, related to :model:`auth.User` when User is Officer that took video.
	"""
	video_id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=128)
	video_date = models.DateTimeField(blank=True, null=True)
	retention = models.CharField(max_length=10)
	upload_date = models.DateTimeField(blank=True, null=True)
	video = models.FileField(upload_to="videos", null=True, blank=True)
	content_type = models.CharField(max_length=50, default="xxx")

	def __unicode__(self):
#		return "%s %s" % (self.first_name, self.last_name)
		return "%s %s" % (self.video_id, self.content_type)

# Request model: handle the extended retention, delete video and make public request
class Request(models.Model):
	TYPE_CHOICES = (('extend_retention', 'extend_retention',), ('delete_video', 'delete_video',), ('make_public', 'make_public',))
	
	request_id = models.AutoField(primary_key=True)
	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES)
	video_id = models.ForeignKey(Video)
	user_id = models.ForeignKey(User)
	reasoning = models.CharField(max_length=1000)

# MeetingRequest model: handle the review meeting request
class MeetingRequest(models.Model):
	request_date = models.DateTimeField(default=timezone.now)
	video_date = models.DateTimeField()
	user_id = models.ForeignKey(User)
	location = models.CharField(max_length=128)
	reasoning = models.CharField(max_length=1000)
