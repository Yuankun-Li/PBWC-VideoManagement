from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from videomanagement.forms import *
import urllib

def login_(request):
    if not request.user.username == '':
        return redirect('/')
    context = {'user': request.user}
    return render(request, 'videomanagement/login.html', context)

@login_required
def logout_(request):
    logout(request)
    return redirect(reverse('login'))

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        print(user.username)
        
def login_manager(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'videomanagement/login_manager.html', context)
    
    form = LoginForm(request.POST)
    context['form'] = form
    
    if not form.is_valid():
        return render(request, 'videomanagement/login_manager.html', context)
    
    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        context['msg'] = "Wrong username or password"
        return render(request, 'videomanagement/login_manager.html', context)