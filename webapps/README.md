# PBWC-VideoManagement/webapps

Use Python2.7 for this project!

To run current program, you need to: 
1. install python-social-auth and social-auth-app-django using command: “pip install python-social-auth” and “pip install social-auth-app-django”. use “—ignore-installed six” if have any problem when uninstalling six.

2. Download and install pyjwkest from: https://github.com/rohe/pyjwkest, get into the directory of pyjwkest and run “python setup.py install”

3. To test that google authentication is enabled, run server locally and visit http://localhost:8000/login/google-oauth2/, which should direct you to the page to log in with google account