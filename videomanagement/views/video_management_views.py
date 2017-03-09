from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from mimetypes import guess_type, MimeTypes

from videomanagement.forms import VideoForm
from videomanagement.models import Video

from datetime import datetime

# Create your views here.


########### VIEWS AND ACTIONS FOR NON-LOGGED IN USERS #######################


########### VIEWS AND ACTIONS FOR LOGGED IN USERS #######################

## Views and Actions for Play_Video Page
# retrieve the content of a video
@login_required
def get_video(request, video_id):
	video = get_object_or_404(Video, video_id=video_id)
	if not video.video:
		raise Http404
	content_type = guess_type(video.video.name)
	print(video.video.name)
	return HttpResponse(video.video, content_type = content_type)

# retrive the page to view a video
@login_required
def view_video(request, video_id):
	context = {'video_id': video_id}
	for g in request.user.groups.all():
		context['group'] = g.name
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
    return render(request,'videomanagement/community_main.html',context)

## Views and Actions for Committe Page

@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_video(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)

    context = {}


    video = Video.objects.get(video_id=video_id)
    video.video.delete()
    video.delete()
    context['message'] = 'video deleted.'

    all_videos = Video.objects.all().order_by('-video_date')
    context['videos'] = all_videos
    return render(request,'videomanagement/community_main.html',context)


########### VIEWS AND ACTIONS FOR VIDEO UPLOADERS #######################


@login_required
@user_passes_test(lambda u: u.groups.filter(name='video_manager').count() == 1, login_url='/')
def upload(request):
    """
    Create an individual :model:`videomanagement.Video`.

    **Context**

    ``Video``
        An instance of :model:`videomanagement.Video`.

    **Template:**

    :template:`videomanagement/upload.html`
    """
    context = {}
    context['user'] = request.user

    # For get method, lead to upload pages
    if request.method == 'GET':
        context['form'] = VideoForm()
        return render(request, 'videomanagement/upload.html', context)

    # For post method, upload file
    new_video = Video(upload_date=datetime.now())
    form = VideoForm(request.POST, request.FILES, instance=new_video)
    if not form.is_valid():
        context['message'] = 'Upload failed'
        context['form'] = form
        return render(request, 'videomanagement/upload.html', context)
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        new_video.content_type = form.cleaned_data['video'].content_type
        form.save()
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
    return render(request,'videomanagement/committee_main.html',context)




