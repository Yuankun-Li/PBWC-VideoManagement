from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from videomanagement.models import *




## retrieve all actions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='committee_member').count() == 1, login_url='/')
def committee_action_retrieve(request):
    """
    Retrieve all instances of :model:`videomanagement.CommitteeAction` from the dB.

    **Context**

    ``CommitteeAction``
    An instance of :model:`videomanagement.CommitteeAction`.

    **Template:**

    :template:`videomanagement/retrieve_actions.html`

    **Description**
    This view retrieves all CommitteeAction objects in the dB. The resulting list of actions is displayed to the user in ascending chronological order by date action was taken.
    """
    context = {}
    actions = CommitteeAction.objects.all()
    
    context['actions'] = actions
    
    groups = request.user.groups.all()
    if len(groups) > 0:
        context['user_type'] = request.user.groups.all()[0].name
    else:
        context['user_type'] = ""
    
    return render(request, 'videomanagement/retrieve_actions.html', context)


