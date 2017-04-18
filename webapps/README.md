# PBWC-VideoManagement/webapps

Use Python2.7 for this project!

To establish an admin user, and subsequently create new users that fit into each stakeholder role, perform the following: 

1. Install docutils using "pip install docutils".

2. Install python-social-auth and social-auth-app-django using the following commands:
        <br/> a. “pip install python-social-auth"
        <br/> b. “pip install social-auth-app-django”
   <br/> Use “—ignore-installed six” if you have any problem when uninstalling six.

3. Download and install pyjwkest from the following URL: https://github.com/rohe/pyjwkest. Get into the directory of pyjwkest and run “python setup.py install”.

4. Install the imageio and moviepy Python packages (if required) with the following commands:
        <br/> a. “pip install imageio"
        <br/> b. “pip install moviepy”
    <br/> If you don't have the latest version of numpy, use the command "pip install numpy --upgrade”. Use “—ignore-installed six” if have any problem when uninstalling six.

5. Use the command “python manage.py createsuperuser” to create an admin account. This will require a username, email, and password.

6. Run the server with command “python manage.py runserver”, and then go to “localhost:8000/admin” in your browser. Here, you can enter the same username and password you just created.

7. Once logged in as a superuser, you can click “Add” next to “Group” (which is under Authentication and Authorization). This will allow you to make new user groups with the appropriate permissions from the listing. Specifically:
        <br/> a. Students:
            <br/> i. “videomanagement | request | Can add request”
            <br/> ii. “videomanagement | request | Can add meeting request”
        <br/> b. Officers:
            <br/> i. “videomanagement | request | Can add request”
            <br/> ii. “videomanagement | request | Can add meeting request”
        <br/> c. Sergeants/Administrative Officials:
            <br/> i. “videomanagement | request | Can add request”
            <br/> ii. “videomanagement | request | Can add meeting request”
            <br/> iii. “videomanagement | video | Can add video"
        <br/> d. Committee Members:
            <br/> i. “videomanagement | request | Can delete request”
            <br/> ii. “videomanagement | request | Can delete meeting request”
            <br/> iii. “videomanagement | video | Can change video"
            <br/> iv. “videomanagement | video | Can delete video"

8. After you have added all stakeholder groups, you can create individual users for each group. Navigate back to Authentication and Authorization, and click “Add” next to “User”. Provide a username and password for this user, and then click "Save".

9. The next page will allow you to enter a first and last name for the user, their email address, and group associations (see Step 5). Users should not receive special permissions beyond those specified by their group.

10. Once you have created all necessary users, you can click "View Site" in the top-right corner of the Django admin screen, and then log in with the credentials you created for each user, one at a time. This will demonstrate the actions that each stakeholder may complete with our web service.




