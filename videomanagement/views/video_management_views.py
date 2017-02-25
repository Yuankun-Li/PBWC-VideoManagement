from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction

from videomanagement.forms import VideoForm
from videomanagement.models import Video

from datetime import datetime

# Create your views here.
@login_required
def upload(request):
    context = {}

    # For get method, lead to upload pages
    if request.method == 'GET':
        context['form'] = VideoForm()
        return render(request, 'videomanagement/upload.html', context)

    # For post method, upload file
    new_video = Video(upload_date=datetime.now())
    form = VideoForm(request.POST, request.FILES, instance=new_video)
    if not form.is_valid():
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