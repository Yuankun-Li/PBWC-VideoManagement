from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

from models import *
from form_validators import validate_committee_user

# MAX_UPLOAD_SIZE need to be set

# VideoForm: Form used in video upload
# Validation need to be fixed
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = { 'location', 'video_date', 'video' }
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
        fields = { 'Date_That_Footage_Was_Recorded', 'Type_of_Request', 'Location_of_Recorded_Event', 'Description_of_Recorded_Event','Reason_for_Request' }
        widgets = {'Date_That_Footage_Was_Recorded': SelectDateWidget(),
                   'Type_of_Request': forms.Select(),
                   'Location_of_Recorded_Event': forms.Select(),
		   'Description_of_Recorded_Event': forms.Textarea(attrs={'placeholder': 'Description of Recorded Event', 'rows': 3, 'cols': '80%'}),
                   'Reason_for_Request': forms.Textarea(attrs={'placeholder': 'Reason for Request', 'rows': 3, 'cols': '80%'})}


#### Committee Action Forms

class ExtendRetentionForm(forms.Form):
	Com1           = forms.CharField(label="Username for Committee Member 1", required=True, validators=[User.username_validator,validate_committee_user])
	Com2           = forms.CharField(label="Username for Committee Member 2", required=True, validators=[User.username_validator,validate_committee_user])
	Com3           = forms.CharField(label="Username for Committee Member 3", required=True, validators=[User.username_validator,validate_committee_user])
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
	class Media:
		css = {'all': 'committeeform.css'}


class InspectVideoForm(forms.Form):
	datasubject = forms.BooleanField(label = "Is the requester present in the video?", required=False)
	legalrep = forms.BooleanField(label = "Is the requester a Legal Representative?", required=False)
	legalrep_role = forms.ChoiceField(label="Requesting Legal Representative is representing", required=False, choices=(
			('', ''),
			('an individual present in the video','an individual present in the video'), 
			('A parent of an individual present in the video','A parent of an individual present in the video'), 
			('the spouse of an individual present in the video','the spouse of an individual present in the video'),
			('the law enforcement officer who recorded the video','the law enforcement officer who recorded the video'),	
			('a client with a reasonable basis to claim video contains exculpatory evidence','a client with a reasonable basis to claim video contains exculpatory evidence')		
))
	community_member     = forms.BooleanField(label="Is the requester a Community Member?", required=False)
	le_officer     = forms.BooleanField(label="Is the requester an officer with community jurisdiction?", required=False)
	le_report = forms.BooleanField(label = "Has the officer filed a report on the incident?", required=False)
	le_recorder     = forms.BooleanField(label="Is the requesting officer the one who recorded the video?", required=False)
	le_superior     = forms.BooleanField(label="Is the requesting officer a superior of the officer who recorded the video?", required=False)
	le_misconduct     = forms.BooleanField(label="Is police misconduct depicted in the video?", required=False)
	class Media:
		css = {'all': 'committeeform.css'}

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

class SearchForm(forms.Form):
    video_date = forms.DateTimeField(widget = SelectDateWidget(attrs={'id': 'video_date'}), required=False)
    location = forms.ChoiceField(choices=[('All','All')] + Video.LOCATION_CHOICES, required=False, widget = forms.Select(attrs={'id': 'location'}))
