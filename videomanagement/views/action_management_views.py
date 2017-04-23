from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from videomanagement.forms import *
from videomanagement.models import *




## retrieve all actions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def committee_action_retrieve(request):
    context = {}
    actions = CommitteeAction.objects.all()
    
    context['actions'] = actions
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    return render(request, 'videomanagement/retrieve_actions.html', context)


