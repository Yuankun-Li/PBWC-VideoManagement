# PBWC-VideoManagement - Project Overview

This is a Django-supported web service for the independent management and disclosure of police body-worn camera (BWC) footage. It has been designed with the privacy of data subjects and accountability of police officers in mind, and is oriented toward deployment of BWCs for the police force of a college or university.

Use of this web service assumes 4 stakeholders: students of the college or university, campus police officers, police "managers" (who are administrative officials in the campus police department), and members of an independent committee (which manages disclosure of BWC footage).

Users in the role of students or campus police officers may log into the web service to view BWC footage captured by campus police officers that independent committee members have approved for disclosure to the college community. These users can also submit requests to the independent committee to:
    <br/> 1. Inspect BWC footage that has not yet been released to the college community (alongside a member of the independent committee).
    <br/> 2. Extend the retention time for BWC footage.
    <br/> 3. Make inaccessible BWC footage that is currently visible to the college community.
    <br/> 4. Make available to the college community specific BWC footage that has not yet been released.

Users in the role of police managers can do the same as students and campus police officers, and are responsible for uploading BWC footage. However, the footage they upload is not visible to them.

Users in the role of independent committee members can do the same as students and campus police officers, and are responsible for resolving all submitted requests. They can also see any footage that police managers have uploaded.

_______________________________________________________________________________________________________________

## How We've Incorporated Privacy and Accountability

1. **Access Control** - We've restricted which pages a specific user can access in accordance with their assigned group (as determined by the Django admin superuser).

2. **Restricted Retention Time** - Any footage that the police managers upload have an automatic retention time of 180 days, after which the footage is deleted. 
<br/> See **PBWC-VideoManagement/videomanagement/views/video_management_views.py** for the implementation.

3. **Video Encryption** - All videos are encrypted with Django's inherent video encryption implementation.
<br/> See **INSERT PATH** for the implementation.

4. **Community Participation** - Users in the role of students and officers can submit requests regarding specific BWC footage to the independent committee, as described above. 
<br/> See **INSERT PATH** for the implementation.

5. **Purpose Specification** - To resolve a submitted request, committee members must complete a form with a series of questions specifically designed for each request type. These questions assist the committee members in determining whether to fulfill or reject the request. These purpose specification forms ensure adherence to the ACLU's Model Act for Use of Body Mounted Cameras by Law Enforcement.
<br/> See **INSERT PATH** for the implementation.

6. **Accountability** - When a committee member fulfills or rejects a request, that action is recorded in a separate audit log. When the independent committee approves a request to make available to the college community specific BWC footage that has not yet been released, that footage becomes visible on the web service for all users.
<br/> See **PBWC-VideoManagement/videomanagement/models.py~** for the implementation of the committee audit log.
<br/> See **INSERT PATH** for the implementation of making specific BWC footage public.

_______________________________________________________________________________________________________________

## User Guide for Testing the Web Service

Please use Python 2.7 for testing.

To establish an admin user, and subsequently create new users that fit into each stakeholder role, perform the following: 

1. Install docutils using "pip install docutils".

2. Install python-social-auth and social-auth-app-django using the following commands:
   * “pip install python-social-auth"
   * “pip install social-auth-app-django”
<br/> Use “—ignore-installed six” if you have any problem when uninstalling six.

3. Download and install pyjwkest from the following URL: https://github.com/rohe/pyjwkest. Get into the directory of pyjwkest and run “python setup.py install”.

4. Install the imageio and moviepy Python packages (if required) with the following commands:
  * “pip install imageio"
  * “pip install moviepy”
<br/> If you don't have the latest version of numpy, use the command "pip install numpy --upgrade”. Use “—ignore-installed six” if have any problem when uninstalling six.

5. Use the command “python manage.py createsuperuser” to create an admin account. This will require a username, email, and password.

6. Run the server with command “python manage.py runserver”, and then go to “localhost:8000/admin” in your browser. Here, you can enter the same username and password you just created.

7. Once logged in as a superuser, you can click “Add” next to “Group” (which is under Authentication and Authorization). This will allow you to make new user groups with the appropriate permissions from the listing. Specifically:
  * Students:
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
  * Officers:
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
  * Police Managers/Administrative Officials (*Group must be labeled "video_manager" for web service to provide users in this group access to the video upload webpage*):
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
    - “videomanagement | video | Can add video"
  * Committee Members (*Group must be labeled "committee_member" for web service to provide users in this group access to the full BWC footage database and all requests submitted by students and officers*):
    - “videomanagement | request | Can delete request”
    - “videomanagement | request | Can delete meeting request”
    - “videomanagement | video | Can change video"
    - “videomanagement | video | Can delete video"

  * **NOTE:** It is **highly discouraged** to change any group name after adding users, as Django will NOT automatically refresh the database to reflect this change. You will be required to do the following if you make such a change:
    - Delete all files in the migration folder.
    - Delete the db.sqlite3 file.
    - Execute the following command: "python manage.py makemigrations".
    - Execute the following command: "python manage.py migrate".
    - Re-establish all user accounts.

8. After you have added all stakeholder groups, you can create individual users for each group. Navigate back to Authentication and Authorization, and click “Add” next to “User”. Provide a username and password for this user, and then click "Save".

9. The next page will allow you to enter a first and last name for the user, their email address, and group associations (see Step 5). Users should not receive special permissions beyond those specified by their group.

10. Once you have created all necessary users, you can click "View Site" in the top-right corner of the Django admin screen, and then log in with the credentials you created for each user, one at a time. This will demonstrate the actions that each stakeholder may complete with our web service.




