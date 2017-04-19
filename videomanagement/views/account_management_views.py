from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from videomanagement.forms import *
import urllib

# log out
@login_required
def logout_(request):
    logout(request)
    return redirect(reverse('login'))

# test log in with OAuth
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        print(user.username)
        
# log in
def login_(request):
    # if already log in, redirect to community page
    if not request.user.username == '':
        return redirect('/')
    context = {'user': request.user}
    # if GET, show log in page
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'videomanagement/login.html', context)
    
    # if POST, validate the form, and log in
    form = LoginForm(request.POST)
    context['form'] = form
    
    # return to log in page with error information if form not valid
    if not form.is_valid():
        return render(request, 'videomanagement/login.html', context)
    
    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    if user is not None:
        login(request, user)
        return redirect('/')
    # return to log in page with error information if could not find the user with given username and password
    else:
        context['msg'] = "Wrong username or password"
        return render(request, 'videomanagement/login.html', context)
