from videomanagement.models import Request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

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