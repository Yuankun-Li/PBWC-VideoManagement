from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
	video_id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=128)
	video_date = models.DateTimeField(blank=True, null=True)
	retention = models.CharField(max_length=10)
	upload_date = models.DateTimeField(blank=True, null=True)
	video = models.FileField(upload_to="videos", null=True, blank=True)
	content_type = models.CharField(max_length=50, default="xxx")

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)