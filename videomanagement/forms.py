from django import forms

from models import *


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = { 'location', 'video_date', 'retention', 'video' }

    def clean_picture(self):
        video = self.cleaned_data['video']
        if not video:
            raise forms.ValidationError('You must upload a video')
        if not video.content_type or not video.content_type.startswith('video'):
            raise forms.ValidationError('File type is not video')
        # if picture.size > MAX_UPLOAD_SIZE:
        #     raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return video