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

1. **Access Control** - We've restricted which pages a specific user can access in accordance with their assigned group (as determined by the Django admin superuser; see testing instructions below for further details).

2. **Restricted Retention Time** - Any footage that the police managers upload have an automatic retention time of 180 days, after which the footage is deleted (though students and officers may request to extend the retention time for specific footage, as noted in the Overview).

3. **Video Encryption** - We use a third-party library that provides methods for encryption upon storage and decryption/fetching of video files upon request.

4. **Community Participation** - Users in the role of students and officers can submit requests regarding specific BWC footage to the independent committee, as noted in the Overview. 

5. **Purpose Specification** - To resolve a submitted request, committee members must complete a form with a series of questions specifically designed for each request type. These questions assist the committee members in determining whether to fulfill or reject the request. These purpose specification forms ensure adherence to the ACLU's Model Act for Use of Body Mounted Cameras by Law Enforcement.

6. **Accountability** - When a committee member fulfills or rejects a request, that action is recorded in a separate audit log. When the independent committee approves a request to make available to the college community specific BWC footage that has not yet been released, that footage becomes visible on the web service for all users.

_______________________________________________________________________________________________________________

## Key Elements of This Repository

**PBWC-VideoManagement/videomanagement/models.py** contains the models that enable video upload, a student's or officer's submission of requests, a committee member's resolution of a request, and the transfer of a committee action to the audit log.

**PBWC-VideoManagement/videomanagement/forms.py** contains code for all forms pertaining to login, video upload, request creation, and all committee request resolution.

**PBWC-VideoManagement/videomanagement/views/account_management_views.py** provides the controller for login.

**PBWC-VideoManagement/videomanagement/views/action_management_views.py** provides the controller to retrieve committee actions.

**PBWC-VideoManagement/videomanagement/views/request_management_views.py** provides the controller for request submission and resolution.

**PBWC-VideoManagement/videomanagement/views/video_management_views.py** provides the controller for video retrieval (which enables viewing) and upload.

**PBWC-VideoManagement/videomanagement/templates/videomanagement/** contains the HTML templates that enable all actions specified in models.py.

**PBWC-VideoManagement/videomanagement/static/videomanagement/js/** contains the purpose specification form logic and media player implementation.

_______________________________________________________________________________________________________________

## User Guide for Testing the Web Service

Please use Python 2.7 for testing.

To establish an admin user, and subsequently create new users that fit into each stakeholder role, perform the following: 

1. Install docutils using "pip install docutils".

2. Install python-social-auth and social-auth-app-django:
   * pip install python-social-auth
   * pip install social-auth-app-django
<br/> Use “—ignore-installed six” if you have any problem when uninstalling six.

3. Download and install pyjwkest from the following URL: https://github.com/rohe/pyjwkest. Get into the directory of pyjwkest and run “python setup.py install”.

4. Viewing GIFs of the BWC footage requires the following:
  * pip install imageio
  * pip install moviepy
<br/> If you don't have the latest version of numpy, use the command "pip install numpy --upgrade”. Use “—ignore-installed six” if have any problem when uninstalling six.

5. Install the Homebrew package manager, which is specifically designed to handle open-source tools (for this project, we need libmagic). You can find instructions on this at the following link: https://www.howtogeek.com/211541/homebrew-for-os-x-easily-installs-desktop-apps-and-terminal-utilities/

6. Install libmagic using "brew install libmagic".

7. File encryption requires the following:
  * pip install python-social-auth
  * export DEFF_SALT="salt"
  * export DEFF_PASSWORD="password"
  * export DEFF_FETCH_URL_NAME="fetch"

8. Use the command “python manage.py createsuperuser” to create an admin account. This will require a username, email, and password.

9. Run the server with command “python manage.py runserver”, and then go to “localhost:8000/admin” in your browser. Here, you can enter the same username and password you just created.

10. Once logged in as a superuser, you can click “Add” next to “Group” (which is under Authentication and Authorization). This will allow you to make new user groups with the appropriate permissions from the listing. Specifically:
  * Students (*Group can be labeled "student"):
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
  * Officers (*Group can be labeled "officer"):
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
  * Police Managers/Administrative Officials (*Group must be labeled "video_manager" for web service to provide users in this group access to the video upload webpage*):
    - “videomanagement | request | Can add request”
    - “videomanagement | request | Can add meeting request”
    - “videomanagement | video | Can add video"
  * Committee Members (*Group must be labeled "committee_member" for web service to provide users in this group access to the full BWC footage database and all requests submitted by students and officers*):
    - "videomanagement | committee action | Can add committee action"
    - "videomanagement | committee action | Can change committee action"
    - "videomanagement | committee action | Can delete committee action"
    - “videomanagement | request | Can change meeting request”
    - “videomanagement | request | Can delete meeting request”
    - “videomanagement | request | Can change request”
    - “videomanagement | request | Can delete request”
    - “videomanagement | video | Can change video"
    - “videomanagement | video | Can delete video"

  * **NOTE:** The site will not function properly if you use a different string for police manager and committee member group names. It is also **highly discouraged** to change the student and officer group names after adding users, as Django will NOT automatically refresh the database to reflect this change. You will be required to do the following if you make such a change:
    - Delete all files in the migration folder.
    - Delete the db.sqlite3 file.
    - Execute the following command: "python manage.py makemigrations".
    - Execute the following command: "python manage.py migrate".
    - Re-establish all user accounts.

11. After you have added all stakeholder groups, you can create individual users for each group. Navigate back to Authentication and Authorization, and click “Add” next to “User”. Provide a username and password for this user, assign them to their respective group user "Permissions", and then click "Save".

12. The next page will allow you to enter a first and last name for the user, their email address, and group associations (see Step 10). Users should not receive special permissions beyond those specified by their group.

13. Once you have created all necessary users, you can click "View Site" in the top-right corner of the Django admin screen, and then log in with the credentials you created for each user, one at a time. This will demonstrate the actions that each stakeholder may complete with our web service. It's best if you navigate the web service in the following manner:

  * First log in as a video manager user and upload a few videos.
  * Next, log in as a student user, and submit a couple requests to make footage public, with the requests matching the location and date of the videos you just uploaded.
  * Then log in as a committee member. Navigate to the tab for pending requests, and work through the purpose specification forms that come up when you attempt to accept the requests.
  * Log back into the student account, and see that the videos for which the student submitted requests are now available.




