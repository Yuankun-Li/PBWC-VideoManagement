from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django_encrypted_filefield.fields import EncryptedFileField, EncryptedImageField

#needed for request acceptance forms
#from forms import MakePublicForm

# Create your models here.

# Video model: Include basic information about upload video information
# retention need to be modified in V2
# content_type need to be fixed

class Video(models.Model):
	LOCATION_CHOICES = (('Gates Center for Computer Science', 'Gates Center for Computer Science',), 
					('Cyert Hall', 'Cyert Hall'),
					('Cohon University Center', 'Cohon University Center'),
					('Hunt Library', 'Hunt Library'),
					('Other place', 'Other place'),
					('Morewood Apartments', 'Morewood Apartments'))
	"""
	Stores a single video entry, related to :model:`auth.User` when User is Officer that took video.
	"""
	video_id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=128, choices=LOCATION_CHOICES, default='Gates Center for Computer Science')
	video_date = models.DateTimeField(blank=True, null=True)
	retention = models.IntegerField()
	upload_date = models.DateTimeField(blank=True, null=True)
	# encrypted filefield
	video = EncryptedFileField(upload_to="videos", blank=True)
	content_type = models.CharField(max_length=50)
	is_public = models.BooleanField(default=False)
	gif = models.ImageField(upload_to="gif", null=True)
	#TODO: Recording Officer ID

	def __unicode__(self):
#		return "%s %s" % (self.first_name, self.last_name)
		return "%s %s" % (self.video_id, self.content_type)

# Request model: handle the extended retention, privatize video, and register complaint request
class Request(models.Model):
	TYPE_CHOICES = (('extend_retention', 'extend_retention'), ('privatize_video','privatize_video'),('register_complaint', 'register_complaint'))
	
	request_id = models.AutoField(primary_key=True)
	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='extend_retention')
	video = models.ForeignKey(Video)
	user = models.ForeignKey(User)
	reasoning = models.CharField(max_length=1000)
	resolved = models.BooleanField(default=False)
	
	# accept a request
	def accept(self, request_id, policy_justification,committee_text_reason):
		self.resolved = True
		self.save()
		
		if self.type == 'privatize_video':
			tmp_video = self.video
			tmp_video.is_public = False
			tmp_video.save()
			new_action = CommitteeAction(type='privatize_video', request_id=request_id, video_id=self.video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()
		elif self.type == 'extend_retention':
			tmp_video = self.video
			tmp_video.retention = 1825
			tmp_video.save()
			new_action = CommitteeAction(type='extend_retention', request_id=request_id, video_id=self.video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()

# MeetingRequest model: handle the review meeting request
class MeetingRequest(models.Model):
	TYPE_CHOICES = (('meeting', 'meeting',), ('make_public', 'make_public',), ('inspect_video', 'inspect_video'))
	

	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='meeting')
	video_date = models.DateTimeField()
	user = models.ForeignKey(User)
	location = models.CharField(max_length=128, choices=Video.LOCATION_CHOICES, default='Gates Center for Computer Science')
	description = models.CharField(max_length=1000)
	reason_for_request = models.CharField(max_length=1000)
	resolved = models.BooleanField(default=False)
	
	# accept a request
	def accept(self, request_id, policy_justification, committee_text_reason):

		self.resolved = True
		self.save()
		#Doesn't currently work: need to re-architect
		if self.type == 'make_public':
			video = get_object_or_404(Video, video_date=self.video_date, location=self.location)
			video.is_public = True
			video.save()
			new_action = CommitteeAction(type='make_public', request_id=request_id, video_id=video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()
		elif self.type == 'inspect_video':
			#notify/email user
			video = get_object_or_404(Video, video_date=self.video_date, location=self.location)
			video.save()
			new_action = CommitteeAction(type='inspect_video', request_id=request_id, video_id=video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()

class CommitteeAction(models.Model):
	TYPE_CHOICES = (('meeting', 'meeting',), ('make_public', 'make_public',), 
('inspect_video', 'inspect_video'),('extend_retention', 'extend_retention'), ('privatize_video','privatize_video'))

	action_id = models.AutoField(primary_key=True)
	action_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='meeting')
	request_id = models.IntegerField()
	video_id = models.IntegerField()
	policy_justification = models.CharField(max_length=1000)
	committee_text_reason = models.CharField(max_length=1000)
	#TODO: recording officer ID







