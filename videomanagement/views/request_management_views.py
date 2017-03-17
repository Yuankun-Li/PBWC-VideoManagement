from videomanagement.models import Request
from django.contrib.auth.decorators import login_required, user_passes_test

## create a request
@login_required
def create_request(request, video_id):
    context['user'] = request.user
    
    # For get method, lead to create request pages
    if request.method == 'GET':
        return render(request, 'videomanagement/create_request.html', context)