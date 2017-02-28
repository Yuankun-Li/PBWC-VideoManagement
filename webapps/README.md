# PBWC-VideoManagement/webapps

Use Python2.7 for this project!

To run current program, you need to: 
0. install docutils using "pip install docutils"

1. install python-social-auth and social-auth-app-django using command: “pip install python-social-auth” and “pip install social-auth-app-django”. use “—ignore-installed six” if have any problem when uninstalling six.

2. Download and install pyjwkest from: https://github.com/rohe/pyjwkest, get into the directory of pyjwkest and run “python setup.py install”

3. To test that google authentication is enabled, run server locally and visit http://localhost:8000/login/google-oauth2/, which should direct you to the page to log in with google account

4. To check regular log in function, first create your admin account locally and create an account, assign the group “video_manager”, with permission to alter video table. Then log in with the “I’m a video manager” button and try out the function. 
