from django import forms
from django.forms.extras.widgets import SelectDateWidget

from models import *

# MAX_UPLOAD_SIZE need to be set

# VideoForm: Form used in video upload
# Validation need to be fixed
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = { 'location', 'video_date', 'retention', 'video' }
        widgets = {'video_date': SelectDateWidget(),
                   'location': forms.Select()}

    def clean_video(self):
        video = self.cleaned_data['video']
        if not video:
            raise forms.ValidationError('You must upload a video')
        if not video.content_type:
          raise forms.ValidationError('File type is not video')
        if not video.content_type.startswith('video/mp4')  and not video.content_type.startswith('video/avi'):
          raise forms.ValidationError('File type is not video')
        # if picture.size > MAX_UPLOAD_SIZE:
        #     raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return video
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 200, 
                               widget = forms.TextInput(attrs={'placeholder': 'Username',
                                                               'class': 'form-control login-register-field',
                                                               'autofocus': 'autofocus'}))
    
    password = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                    'class': 'form-control login-register-field'}))
    
class CreateRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = { 'type', 'reasoning' }
        widgets = {'type': forms.Select(),
                   'reasoning': forms.Textarea(attrs={'placeholder': 'Reasons', 'rows': 3, 'cols': '80%'})}
        
class CreateMeetingRequestForm(forms.ModelForm):
    class Meta:
        model = MeetingRequest
        fields = { 'video_date', 'type', 'location', 'reasoning' }
        widgets = {'video_date': SelectDateWidget(),
                   'type': forms.Select(),
                   'location': forms.Select(),
                   'reasoning': forms.Textarea(attrs={'placeholder': 'Reasons', 'rows': 3, 'cols': '80%'})}


#### Committee Action Forms

class ExtendRetentionForm(forms.Form):
	le_officer     = forms.BooleanField(label="Is the requester a Law Enforcement Officer?", required=False)
	le_trainingpurpose = forms.BooleanField(label = "Is the request for training purposes?", required=False)
	le_Evidexculp = forms.BooleanField(label = "Is there Evidentiary or Exculpatory Value?", required=False)
	
	le_role = forms.ChoiceField(label="Requester is", required=False, choices=(
			('', ''),
			('the Recording Officer','the Recording Officer'), 
			('Present in the Video','Present in the Video'), 
			('Superior Officer of Recording Officer','Superior Officer of Recording Officer')))

	datasubject = forms.BooleanField(label = "Is the requester a Data Subject?", required=False)

	## FeatureExtension: Incorporate Additional Policy Clauses

	rationale = forms.CharField(max_length=1000,
			widget = forms.TextInput(attrs={'placeholder': 'Rationale',
                                                                    'class': 'form-control'}))


class InspectVideoForm(forms.Form):
	datasubject = forms.BooleanField(label = "Is the requester present in the video?", required=False)
	community_member     = forms.BooleanField(label="Is the requester a Community Member?", required=False)
	le_officer     = forms.BooleanField(label="Is the requester a law enforcement officer with jurisdiction over the community?", required=False)
	le_report = forms.BooleanField(label = "Has the officer filed a report on the incident?", required=False)
	le_recorder     = forms.BooleanField(label="Is the requesting officer the one who recorded the video?", required=False)
	le_superior     = forms.BooleanField(label="Is the requesting officer a superior of the officer who recorded the video?", required=False)
	le_misconduct     = forms.BooleanField(label="Has there been a complaint of police misconduct regarding the events depicted in the video?", required=False)

	legalrep = forms.BooleanField(label = "Is the requester a Legal Representative?", required=False)
	legalrep_role = forms.ChoiceField(label="Requesting Legal Representative is representing", required=False, choices=(
			('', ''),
			('an individual present in the video','an individual present in the video'), 
			('A parent of an individual present in the video','A parent of an individual present in the video'), 
			('the spouse of an individual present in the video','the spouse of an individual present in the video'),
			('the law enforcement officer who recorded the video','the law enforcement officer who recorded the video'),	
			('a client with a reasonable basis to claim video contains exculpatory evidence','a client with a reasonable basis to claim video contains exculpatory evidence')		
))

	## FeatureExtension: Incorporate Additional Policy Clauses

	rationale = forms.CharField(max_length=1000,
			widget = forms.TextInput(attrs={'placeholder': 'Rationale',
                                                                    'class': 'form-control'}))

class PrivatizeVideoForm(forms.Form):
	rationale = forms.CharField(max_length=1000,
			widget = forms.TextInput(attrs={'placeholder': 'Rationale',
                                                                    'class': 'form-control'}))

class DeleteVideoForm(forms.Form):
	rationale = forms.CharField(max_length=1000,
			widget = forms.TextInput(attrs={'placeholder': 'Rationale',
                                                                    'class': 'form-control'}))


class MakePublicForm(forms.Form):
	purpose = forms.ChoiceField(choices=(
			('Use of Force','Use of Force'), 
			('Registered Complaint','Registered Complaint'), 
			('Overriding Public Interest','Overriding Public Interest')))

	rationale = forms.CharField(max_length=1000,
			widget = forms.TextInput(attrs={'placeholder': 'Rationale',
                                                                    'class': 'form-control'}))

