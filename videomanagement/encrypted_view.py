
from django_encrypted_filefield.views import FetchView

class MyPermissionRequiredMixin():
	"""
	Your own rules live here
	"""
	pass


class MyFetchView(MyPermissionRequiredMixin, FetchView):
	pass