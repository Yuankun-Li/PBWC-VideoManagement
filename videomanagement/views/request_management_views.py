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
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
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
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_request(request, request_id):
    # get the request to delete
    req = get_object_or_404(Request, request_id=request_id)
    context = {}
    
    req.delete()
    return redirect(reverse('retrieve_requests'))

# retrieve extend retention request webpage
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def extend_retention(request, request_id):
    context = {}
    context['request_id'] = request_id
    context['form'] = ExtendRetentionForm()
    # either retrieve the request object, or return 404 error
    req = get_object_or_404(Request, request_id=request_id)
    context['video_id'] = req.video
    return render(request, 'videomanagement/extend_retention.html', context)


# retrieve privatize video from public request webpage
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def privatize_video(request, request_id):
    context = {}
    context['request_id'] = request_id
    context['form'] = PrivatizeVideoForm()
    # either retrieve the request object, or return 404 error
    req = get_object_or_404(Request, request_id=request_id)
    return render(request, 'videomanagement/privatize_video.html', context)

# retrieve delete video request webpage
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_video_request(request, request_id):
    context = {}
    context['request_id'] = request_id
    context['form'] = DeleteVideoForm()
    # either retrieve the request object, or return 404 error
    req = get_object_or_404(Request, request_id=request_id)
    return render(request, 'videomanagement/delete_video.html', context)

# accept a Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def accept_request(request, request_id):
    # get the request to accept
    context = {}
    req = get_object_or_404(Request, request_id=request_id)
    if req.type == "privatize_video":
        form = PrivatizeVideoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            policy_justification = "none"
            committee_text_reason = data['rationale']
            context['message'] = 'Action created'
            req.accept(request_id, policy_justification,committee_text_reason)
            return render(request,'videomanagement/retrieve_actions.html',context)
    if req.type == "extend_retention":
	form = ExtendRetentionForm(request.POST)
    	if form.is_valid():
		data = form.cleaned_data
		policy_justification = data['le_officer']
		committee_text_reason = data['rationale']
        	context['message'] = 'Action created'
    		req.accept(request_id, policy_justification,committee_text_reason)
    		return render(request,'videomanagement/retrieve_actions.html',context)
    return redirect(reverse('retrieve_requests'))


#### Meeting Request Views

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
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def retrieve_meeting_requests(request):
    context = {}
    context['user'] = request.user
    
    requests = MeetingRequest.objects.all()
    
    videos_for_request = []
    for re in requests:
        request_video = {}
        videos = Video.objects.all().filter(video_date=re.video_date, location=re.location)
        request_video['videos'] = videos
        request_video['request'] = re
        videos_for_request.append(request_video)
    
    context['requests'] = videos_for_request
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_meeting_requests.html', context)


# delete a meeting Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_meeting_request(request, id):
    # get the request to delete
    req = get_object_or_404(MeetingRequest, id=id)
    context = {}
    
    req.delete()
    return redirect(reverse('retrieve_meeting_requests'))


# retrieve make public meeting request webpage
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def make_public(request, request_id):
    context = {}
    context['meeting_request_id'] = request_id
    context['form'] = MakePublicForm()
    # either retrieve the request object, or return 404 error
    req = get_object_or_404(MeetingRequest, id=request_id)
    context['video_date'] = req.video_date
    return render(request, 'videomanagement/make_public.html', context)

# retrieve inspect video meeting request webpage
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def inspect_video(request, request_id):
    context = {}
    context['meeting_request_id'] = request_id
    context['form'] = InspectVideoForm()
    # either retrieve the request object, or return 404 error
    req = get_object_or_404(MeetingRequest, id=request_id)
    context['video_date'] = req.video_date
    return render(request, 'videomanagement/inspect_video.html', context)

# accept a meeting Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def accept_meeting_request(request, id):
    # get the request to accept
    if request.method == "POST":
    	req = get_object_or_404(MeetingRequest, id=id)
	if req.type == "make_public":
		form = MakePublicForm(request.POST)
		if form.is_valid():
    			req.accept()
    return redirect(reverse('retrieve_meeting_requests'))



