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
	"""
	Stores a single video entry, related to :model:`auth.User` when User is Officer that took video.
	"""
	LOCATION_CHOICES = [('Gates Center for Computer Science', 'Gates Center for Computer Science',), 
					('Cyert Hall', 'Cyert Hall'),
					('Cohon University Center', 'Cohon University Center'),
					('Hunt Library', 'Hunt Library'),
					('Other place', 'Other place'),
					('Morewood Apartments', 'Morewood Apartments')]
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
	"""
	Stores a single Request entry, related to :model:`auth.User` where User is requesting user, and :model:`videomanagement.Video` where Video is the one on which the User is making a Request.
	"""
	TYPE_CHOICES = (('extend_retention', 'Extend Retention Time'), ('privatize_video','Remove This Video from the Public Page'),('register_complaint', 'Register a General Complaint'))
	
	request_id = models.AutoField(primary_key=True)
	request_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='extend_retention')
	video = models.ForeignKey(Video)
	user = models.ForeignKey(User)
	reasoning = models.CharField(max_length=1000)
	resolved = models.BooleanField(default=False)
	accepted = models.BooleanField(default=False)
	
	# accept a request
	def accept(self, request_id, policy_justification,committee_text_reason):
		"""
		Accepts the corresponding Request, marks it as resolved, affects the action corresponding to its type (Make Video Private, or Extend Retention Time), and creates and saves a CommitteeAction in the dB
		"""
		self.resolved = True
		self.accepted = True
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

	# reject a request
	def reject(self, request_id, policy_justification,committee_text_reason):
		"""
		Denies the corresponding Request, and marks the Request as resolved.
		"""
		self.resolved = True
		self.save()
		new_action = CommitteeAction(type='extend_retention', request_id=request_id, video_id=self.video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
		new_action.save()

	def justify_extend(self, data, policy_justification):
		"""
		This function provides the logic validating that the Committee's Action to accept or deny the extension of retention is justified by the policy outlined in the Best Practices.
		"""
		justify_deny = False
		justify_accept = False

		if data['datasubject'] is True:	
			justify_accept=True
			policy_justification = "Extension approved by Section 6.f, ACLU clause 1.j.2.E"
		else:
			if data['le_officer'] is True:
				if data['le_trainingpurpose'] is False:
					if data['le_Evidexculp'] is False:
						justify_deny=True
						policy_justification = "Extension denied by Section 6.f, ACLU clause 1.j.2"
					elif data['le_Evidexculp'] is True:
						if data['le_role'] == 'the Recording Officer':
							justify_accept=True
							policy_justification = "Extension approved by Section 6.f, ACLU clause 1.j.2.A"	
						elif data['le_role'] == 'Present in the Video':
							justify_accept=True
							policy_justification = "Extension approved by Section 6.f, ACLU clause 1.j.2.B"	
						elif data['le_role'] == 'Superior Officer of Recording Officer':
							justify_accept=True
							policy_justification = "Extension approved by Section 6.f, ACLU clause 1.j.2.C"	
						else:
							justify_deny=True
							policy_justification = "Extension denied by Section 6.f, ACLU clause 1.j.2.D"	
				elif data['le_trainingpurpose'] is True:
					justify_accept=True
					policy_justification = "Extension approved by Section 6.f, ACLU clause 1.j.2.D"
			else:
				justify_deny=True
				policy_justification = "Extension denied by Section 6.f, ACLU clause 1.j.2"
			#consider adding functionality from ACLU policy 1.j.2.F,G, and witness/evidentiary/exculpatory value	
			#else: 
		return justify_accept,justify_deny, policy_justification

	

# MeetingRequest model: handle the review meeting request
class MeetingRequest(models.Model):
	"""
	Stores a single MeetingRequest entry, related to :model:`auth.User` where User is requesting user.
	"""
	TYPE_CHOICES = (('make_public', 'Make The Referred Video Public',), ('inspect_video', 'Inspect a Video'))
	
	request_date = models.DateTimeField(default=timezone.now)
	Type_of_Request = models.CharField(max_length=50, choices=TYPE_CHOICES, default='meeting')
	Date_That_Footage_Was_Recorded = models.DateTimeField()
	user = models.ForeignKey(User)
	Location_of_Recorded_Event = models.CharField(max_length=128, choices=Video.LOCATION_CHOICES, default='Gates Center for Computer Science')
	Description_of_Recorded_Event = models.CharField(max_length=1000)
	Reason_for_Request = models.CharField(max_length=1000)
	resolved = models.BooleanField(default=False)
	accepted = models.BooleanField(default=False)
	
	# accept a request
	def accept(self, request_id, policy_justification, committee_text_reason):
		"""
		Accepts the corresponding MeetingRequest, marks it as resolved, affects the action corresponding to its type (Makes the Video Public, or allows Video Inspection), and creates and saves a CommitteeAction in the dB
		"""
		self.resolved = True
		self.accepted = True
		self.save()
		if self.Type_of_Request == 'make_public':
			video = get_object_or_404(Video, video_date=self.Date_That_Footage_Was_Recorded, location=self.Location_of_Recorded_Event )
			video.is_public = True
			video.save()
			new_action = CommitteeAction(type='make_public', request_id=request_id, video_id=video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()
		elif self.Type_of_Request == 'inspect_video':
			#notify/email user
			video = get_object_or_404(Video, video_date=self.Date_That_Footage_Was_Recorded, location=self.Location_of_Recorded_Event )
			video.save()
			new_action = CommitteeAction(type='inspect_video', request_id=request_id, video_id=video.video_id, policy_justification=policy_justification, committee_text_reason=committee_text_reason)
			new_action.save()

	# reject a request
	def reject(self, request_id):
		"""
		Denies the corresponding MeetingRequest, and marks the MeetingRequest as resolved.
		"""
		self.resolved = True
		self.save()

class CommitteeAction(models.Model):
	"""
	Stores a single committeeaction entry. This table is designed to be de-coupled from other tables in site and potentially extant in a separate database, so no ID fields (request_id, video_id) are foreign keys.
	"""
	TYPE_CHOICES = (('make_public', 'Make Video Public',), 
('inspect_video', 'Inspect Video'),('extend_retention', 'Extend Retention Time'), ('privatize_video','Make Video Private'))

	action_id = models.AutoField(primary_key=True)
	action_date = models.DateTimeField(default=timezone.now)
	type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='meeting')
	request_id = models.IntegerField()
	video_id = models.IntegerField()
	policy_justification = models.CharField(max_length=1000)
	committee_text_reason = models.CharField(max_length=1000)
	#TODO: recording officer ID







