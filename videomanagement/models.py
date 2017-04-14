from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#needed for request acceptance forms
#from forms import MakePublicForm

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
	retention = models.IntegerField()
	upload_date = models.DateTimeField(blank=True, null=True)
	video = models.FileField(upload_to="videos", blank=True)
	content_type = models.CharField(max_length=50)
	is_public = models.BooleanField(default=False)
	gif = models.ImageField(upload_to="gif", null=True)

	def __unicode__(self):
#		return "%s %s" % (self.first_name, self.last_name)
		return "%s %s" % (self.video_id, self.content_type)

# Request model: handle the extended retention, delete video and make public request
class Request(models.Model):
	TYPE_CHOICES = (('extend_retention', 'extend_retention',), ('delete_video', 'delete_video',))
	
	request_id = models.AutoField(primary_key=True)
	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='extend_retention')
	video = models.ForeignKey(Video)
	user = models.ForeignKey(User)
	reasoning = models.CharField(max_length=1000)
	
	# accept a request
	def accept(self):
		if self.type == 'delete_video':
			self.video.video.delete()
    			self.video.delete()
		elif self.type == 'extend_retention':
			self.video.retention = 10


# MeetingRequest model: handle the review meeting request
class MeetingRequest(models.Model):
	TYPE_CHOICES = (('meeting', 'meeting',), ('make_public', 'make_public',))
	
	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='meeting')
	video_date = models.DateTimeField()
	user = models.ForeignKey(User)
	location = models.CharField(max_length=128)
	reasoning = models.CharField(max_length=1000)
	
	# accept a request
	def accept(self):
		#Doesn't currently work: need to re-architect
		if self.type == 'make_public':

			video = get_object_or_404(Video, video_date=self.video_date, location=self.location)
			video.is_public = True
			video.save()







