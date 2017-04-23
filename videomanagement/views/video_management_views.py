from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from mimetypes import guess_type, MimeTypes

from videomanagement.forms import VideoForm
from videomanagement.models import Video

from datetime import datetime, timedelta
import imageio
from django.core.files import File
import os

import subprocess

from django.conf import settings
from copy import deepcopy

import tempfile

imageio.plugins.ffmpeg.download()

from moviepy.editor import *


# Create your views here.


########### VIEWS AND ACTIONS FOR NON-LOGGED IN USERS #######################

def privacy_policy(request):
    context = {}
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
	return render(request,'videomanagement/privacy_policy.html',context)

########### VIEWS AND ACTIONS FOR LOGGED IN USERS #######################

## Views and Actions for Play_Video Page
# retrieve the content of a video
@login_required
def get_video(request, video_id):
    	"""
    	Retrieve an instance of :model:`videomanagement.Video` from the dB.

    	**Context**

    	``Video``
        An instance of :model:`videomanagement.Video`.
    	"""
	video = get_object_or_404(Video, video_id=video_id)
	if not video.video:
		raise Http404
	content_type = guess_type(video.video.name)
	return HttpResponse(video.video, content_type = content_type)

# retrive the page to view a video
@login_required
def view_video(request, video_id):
    	"""
    	View an instance of :model:`videomanagement.Video`.

    	**Context**

    	``Video``
        	An instance of :model:`videomanagement.Video`.

    	**Template:**

    	:template:`videomanagement/view_video.html`
    	"""
	context = {'video_id': video_id, 'video': get_object_or_404(Video, video_id=video_id)}
    
	for g in request.user.groups.all():
		context['user_type'] = g.name
    
	return render(request,'videomanagement/view_video.html',context)

## Views and Actions for Community Page

#@login_required
def community_retrieve(request):
    """
    Display all :model:`videomanagement.Video` visible by community members.

    **Context**

    ``videos``
        A collection of :model:`videomanagement.Video`.

    **Template:**

    :template:`videomanagement/community_main.html`
    """
    all_videos = Video.objects.all().order_by('-video_date')
    context = {'videos':all_videos}
    for video in all_videos:
    	this_video = FileSystemStorage(location=settings.BASE_DIR)
    	retention = video.retention
    	time = this_video.created_time(video.video.name)
    	time_now = datetime.now()-timedelta(days=retention)
    	if time_now > time:
    		video.video.delete()
    		video.delete()
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    return render(request, 'videomanagement/community_main.html',context)

## Views and Actions for Committee

@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_video(request, video_id):
    """
    Delete an individual :model:`videomanagement.Video`.

    **Context**

    ``Video``
        An instance of :model:`videomanagement.Video`.

    """
    video = get_object_or_404(Video, video_id=video_id)

    context = {}


    video.is_public = False
    video.save()
    context['message'] = 'remove video from public.'

    all_videos = Video.objects.all().order_by('-video_date')
    context['videos'] = all_videos
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    return render(request,'videomanagement/community_main.html',context)


########### VIEWS AND ACTIONS FOR VIDEO UPLOADERS #######################


@login_required
@user_passes_test(lambda u: u.groups.filter(name='video_manager').count() == 1, login_url='/')
def upload(request):
    """
    Create an individual :model:`videomanagement.Video` from a given videoFile, and generate a gif of that video to display on the community page using the :view:`videomanagement.get_gif` action.

    **Context**

    ``Video``
        An instance of :model:`videomanagement.Video`.

    **Template:**

    :template:`videomanagement/upload.html`
    """
    context = {}
    context['user'] = request.user
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""

    # For get method, lead to upload pages
    if request.method == 'GET':
        context['form'] = VideoForm()
        return render(request, 'videomanagement/upload.html', context)

    # For post method, upload file

    new_video = Video(upload_date=datetime.now(), retention=180)
    form = VideoForm(request.POST, request.FILES, instance=new_video)

    if not form.is_valid():
        context['message'] = 'Upload failed'
        context['form'] = form
        return render(request, 'videomanagement/upload.html', context)
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        
        #copy uploaded temp file data
        data = request.FILES['video']
        data2 = deepcopy(data)

        new_video.content_type = form.cleaned_data['video'].content_type
        form.save()


        # write decrypted data into an tmp file
        # this file will be used for creating gits
        tup = tempfile.mkstemp()
        f = os.fdopen(tup[0], 'w')
        f.write(data2.read())
        f.close()
        filepath = tup[1]
        
        # generate gif for community page from the uploaded video
        #print(new_video.video.path)
        if new_video.content_type.startswith('video/avi'):
            print new_video.video.name
            print new_video.video.name+'.mp4'
            subprocess.call(['./ffmpeg', '-i', new_video.video.name,'-strict', '-2', new_video.video.name+'.mp4'])
            os.remove(new_video.video.name)
            new_video.video=new_video.video.name+'.mp4'
            new_video.content_type = 'video/mp4'
            new_video.save()

        clip = (VideoFileClip(filepath).subclip((0,0.00),(0,0.01)).resize(0.5))
        clip.write_gif("gif/tmp.gif")
        
        gif = File(open("gif/tmp.gif", "rb"))
        name = new_video.video.name
        new_name = name[name.rfind('/') + 1:name.rfind('.')] + ".gif"
        new_video.gif.save(new_name, gif, save=True)
        os.remove("gif/tmp.gif")
        
        context['message'] = 'Item saved.'
        
        context['form'] = VideoForm()

    # For test purpose, render might need to changed
    return render(request, 'videomanagement/upload.html', context)


########### VIEWS AND ACTIONS FOR COMMITTEE MEMBERS #######################


@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def committee_retrieve(request):
    """
    Display all :model:`videomanagement.Video` visible by committee members.

    **Context**

    ``videos``
        A collection of :model:`videomanagement.Video`.

    **Template:**

    :template:`videomanagement/committee_main.html`
    """
    all_videos = Video.objects.all().order_by('-video_date')
    context = {'videos':all_videos}
    for video in all_videos:
    	this_video = FileSystemStorage(location=settings.BASE_DIR)
    	retention = video.retention
    	time = this_video.created_time(video.video.name)
    	time_now = datetime.now()-timedelta(days=retention)
    	if time_now > time:
    		video.video.delete()
    		video.delete()
    return render(request,'videomanagement/committee_main.html',context)

# retrieve the gif of a video
@login_required
def get_gif(request, video_id):
    	"""
    	Retrieves the gif field from the given :model:`videomanagement.Video`.

    	**Context**

    	``Video``
        	An instance of :model:`videomanagement.Video`.
    	"""
	video = get_object_or_404(Video, video_id=video_id)
	if not video.video:
		raise Http404
	gif = video.gif
	content_type = guess_type(gif.name)
	return HttpResponse(gif, content_type = content_type)

