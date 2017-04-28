from videomanagement.models import Request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from videomanagement.forms import *
from videomanagement.models import *

########### VIEWS AND ACTIONS FOR LOGGED IN USERS #######################

## Views and Actions for request on a specific video
## create a request
@login_required
def create_request(request, video_id):
    context = {}
    context['user'] = request.user
    context['video_id'] = video_id
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    # For get method, lead to create request pages
    if request.method == 'GET':
        context['form'] = CreateRequestForm()
        return render(request, 'videomanagement/create_request.html', context)

    # For post method, create request
    # retrieve the video that request is for
    video = get_object_or_404(Video, video_id=video_id)
    new_request = Request(video=video, user=request.user)
    # get the create request form
    form = CreateRequestForm(request.POST, instance=new_request)
    # handle invalid form
    if not form.is_valid():
        context['form'] = form
        return render(request, 'videomanagement/create_request.html', context)
    # save the new request
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
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    # get all videos
    videos = Video.objects.all()
    # get request for each video
    for video in videos:
        requests = Request.objects.filter(video=video, resolved=False)
        if len(requests) > 0:
            requests_by_id[video] = requests
    
    context['requests'] = requests_by_id
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_requests.html', context)

## retrieve all requests made by current user
@login_required
@user_passes_test(lambda u: u.groups.filter(name='student').count() == 1 or u.groups.filter(name='officer').count() == 1, login_url='/')
def retrieve_made_requests(request):
    context = {}
    context['user'] = request.user
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    # get all requests
    requests = request.user.request_set.all()
    
    context['requests'] = requests
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_made_requests.html', context)

# delete a Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_request(request, request_id):
    # get the request to delete
    req = get_object_or_404(Request, request_id=request_id)
    context = {}
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    # delete the request
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
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
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
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    return render(request, 'videomanagement/privatize_video.html', context)

# # retrieve delete video request webpage
# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
# def delete_video_request(request, request_id):
#     context = {}
#     context['request_id'] = request_id
#     context['form'] = DeleteVideoForm()
#     # either retrieve the request object, or return 404 error
#     req = get_object_or_404(Request, request_id=request_id)
#     return render(request, 'videomanagement/delete_video.html', context)

# accept a Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def accept_request(request, request_id):
    # get the request to accept
    context = {}
    actions = CommitteeAction.objects.all()
    context['request_id'] = request_id
    context['actions'] = actions
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    requests_by_id = {}
    
    req = get_object_or_404(Request, request_id=request_id)
    if req.type == "privatize_video":
        form = PrivatizeVideoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            policy_justification = "none"
            committee_text_reason = data['rationale']
	    print "passed"
            if 'accept' in request.POST:
        	context['message'] = "Request Accepted."
                req.accept(request_id, policy_justification,committee_text_reason)
            elif 'reject' in request.POST:
        	context['message'] = "Request Rejected."
                req.reject(id)
#    	    return render(request,'videomanagement/privatize_video.html',context)
    if req.type == "extend_retention":
	form = ExtendRetentionForm(request.POST)
    	if form.is_valid():
		data = form.cleaned_data
		policy_justification = "none"
		committee_text_reason = data['rationale']
                if 'accept' in request.POST:
        	      context['message'] = "Request Accepted."
    		      req.accept(request_id, policy_justification,committee_text_reason)
                elif 'reject' in request.POST:
        	    context['message'] = "Request Rejected."
                    req.reject(id)

## Re-do retrieve-requests in order to obtain updated list of requests
    # get all videos
    videos = Video.objects.all()
    # get request for each video
    for video in videos:
        requests = Request.objects.filter(video=video, resolved=False)
        if len(requests) > 0:
            requests_by_id[video] = requests
    
    context['requests'] = requests_by_id
#    	        return render(request,'videomanagement/extend_retention.html',context)
    return render(request, 'videomanagement/retrieve_requests.html', context)




## Views and Actions for request based on time and location

## create a meeting request
@login_required
def create_meeting_request(request):
    context = {}
    context['user'] = request.user
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
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
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    requests = MeetingRequest.objects.all()
    
    videos_for_request = []
    for re in requests:
        if not re.resolved:
            request_video = {}
            videos = Video.objects.all().filter(video_date=re.Date_That_Footage_Was_Recorded, location=re.Location_of_Recorded_Event)
            request_video['videos'] = videos
            request_video['request'] = re
            videos_for_request.append(request_video)
    
    context['requests'] = videos_for_request
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_meeting_requests.html', context)

## retrieve all meeting requests made by current user
@login_required
@user_passes_test(lambda u: u.groups.filter(name='student').count() == 1 or u.groups.filter(name='officer').count() == 1, login_url='/')
def retrieve_meeting_made_requests(request):
    context = {}
    context['user'] = request.user
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    # get all requests
    requests = request.user.meetingrequest_set.all()
    
    context['requests'] = requests
    
    # For test purpose, render might need to changed
    return render(request, 'videomanagement/retrieve_meeting_made_requests.html', context)

# delete a meeting Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def delete_meeting_request(request, id):
    # get the request to delete
    req = get_object_or_404(MeetingRequest, id=id)
    context = {}
    
    req.delete()
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
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
    context['video_date'] = req.Date_That_Footage_Was_Recorded
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
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
    context['video_date'] = req.Date_That_Footage_Was_Recorded
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    return render(request, 'videomanagement/inspect_video.html', context)

# accept a meeting Request
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def accept_meeting_request(request, id):
    # get the request to accept
    context = {}
    actions = CommitteeAction.objects.all()
    context['request_id'] = id
    context['actions'] = actions
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    if request.method == 'POST':
    	req = get_object_or_404(MeetingRequest, id=id)
	if req.Type_of_Request == "make_public":
		form = MakePublicForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
            		policy_justification = "none"
            		committee_text_reason = data['rationale']
			if 'accept' in request.POST:
        	      		context['message'] = "Request Accepted."
				req.accept(id, policy_justification,committee_text_reason)
                        elif 'reject' in request.POST:
       			    context['message'] = "Request Accepted."
                            req.reject(id)
#            		return render(request,'videomanagement/retrieve_actions.html',context)
	if req.Type_of_Request == "inspect_video":
		form = InspectVideoForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
            		policy_justification = "none"
            		committee_text_reason = data['rationale']

                        if 'accept' in request.POST:
        	      	       context['message'] = "Request Accepted."
            	               req.accept(id, policy_justification,committee_text_reason)
                        elif 'reject' in request.POST:
        	      	    context['message'] = "Request Accepted."
                            req.reject(id)
# Re-do retrieve-meeting-requests in order to obtain updated request list
    requests = MeetingRequest.objects.all()
    
    videos_for_request = []
    for re in requests:
        if not re.resolved:
            request_video = {}
            videos = Video.objects.all().filter(video_date=re.Date_That_Footage_Was_Recorded, location=re.Location_of_Recorded_Event)
            request_video['videos'] = videos
            request_video['request'] = re
            videos_for_request.append(request_video)
    
    context['requests'] = videos_for_request
    return render(request, 'videomanagement/retrieve_meeting_requests.html', context)




