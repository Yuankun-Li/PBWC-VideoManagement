from django.shortcuts import render

def login(request):
    context = {'user': request.user}
    return render(request, 'videomanagement/login.html', context)