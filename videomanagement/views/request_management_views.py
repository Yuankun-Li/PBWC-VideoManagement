from videomanagement.models import Request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from videomanagement.forms import *
from videomanagement.models import *

## create a request
@login_required
def create_request(request, video_id):
    context = {}
    context['user'] = request.user
    context['video_id'] = video_id
    
    # For get method, lead to create request pages
    if request.method == 'GET':
        context['form'] = CreateRequestForm()
        return render(request, 'videomanagement/create_request.html', context)

    # For post method, create request
    video = get_object_or_404(Video, video_id=video_id)
    new_request = Request(video=video, user=request.user)
    form = CreateRequestForm(request.POST, instance=new_request)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'videomanagement/create_request.html', context)
    else:
        form.save()
        context['message'] = 'Request created.'
        context['form'] = CreateRequestForm()
        
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/create_request.html', context)

## retrieve all requests
@login_required
def retrieve_requests(request):
    context = {}
    context['user'] = request.user
    requests_by_id = {}
    
    # get all videos
    videos = Video.objects.all()
    # get request for each video
    for video in videos:
        requests = Request.objects.filter(video=video)
        requests_by_id[video] = requests
    
    context['requests'] = requests_by_id
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_requests.html', context)

# delete a Request
@login_required
def delete_request(request, request_id):
    # get the request to delete
    req = get_object_or_404(Request, request_id=request_id)
    context = {}
    
    req.delete()
    return redirect(reverse('retrieve_requests'))

## create a meeting request
@login_required
def create_meeting_request(request):
    context = {}
    context['user'] = request.user
    
    # For get method, lead to create request pages
    if request.method == 'GET':
        context['form'] = CreateMeetingRequestForm()
        return render(request, 'videomanagement/create_meeting_request.html', context)

    # For post method, create request
    new_request = MeetingRequest(user=request.user)
    form = CreateMeetingRequestForm(request.POST, instance=new_request)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'videomanagement/create_meeting_request.html', context)
    else:
        form.save()
        context['message'] = 'Request created.'
        context['form'] = CreateMeetingRequestForm()
        
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/create_meeting_request.html', context)

## retrieve all meeting requests
@login_required
def retrieve_meeting_requests(request):
    context = {}
    context['user'] = request.user
    
    requests = MeetingRequest.objects.all()
    
    context['requests'] = requests
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_meeting_requests.html', context)

# delete a meeting Request
@login_required
def delete_meeting_request(request, id):
    # get the request to delete
    req = get_object_or_404(MeetingRequest, id=id)
    context = {}
    
    req.delete()
    return redirect(reverse('retrieve_meeting_requests'))