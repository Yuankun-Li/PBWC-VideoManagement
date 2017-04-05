# PBWC-VideoManagement/webapps

Use Python2.7 for this project!

To run current program, you need to: 
0. install docutils using "pip install docutils"

1. install python-social-auth and social-auth-app-django using command: “pip install python-social-auth” and “pip install social-auth-app-django”. use “—ignore-installed six” if have any problem when uninstalling six.

2. Download and install pyjwkest from: https://github.com/rohe/pyjwkest, get into the directory of pyjwkest and run “python setup.py install”

3. Use command “python manage.py createsuperuser” to create an admin account. Then run the server with command “python manage.py runserver” and go to “localhost:8000/admin”. Click the “add” next to “Group”, add a group with name “video_manager”, and give permission “videomanagement | video | Can add video”. Create another group “committee_member” with permission “videomanagement | video | Can delete video”. Add two users, one select “video_manager” as group, and one select “committee_member” as group. 

4. install moviepy using “pip install moviepy”. update numpy if not latest version with “pip install numpy --upgrade”, use “—ignore-installed six” if have any problem when uninstalling six.
