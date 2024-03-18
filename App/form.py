from django.forms import ModelForm
from django import forms
from .models import *
from django.forms import inlineformset_factory



class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name','email_author','phone_author','cni', 'author_profile', 'about_author', 'ville']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['featured_image', 'featured_video', 'title', 'category', 'level', 'language', 'description', 'price', 'discount', 'deadline', 'certificate']

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = objectif
        fields = ['points']

class LessonForm(forms.ModelForm):
    class Meta:
        model = lesson
        fields = ['name']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['serial_number', 'thumbnail', 'youtube_id', 'title', 'time_duration', 'preview']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thumbnail'].required = False  
        
ObjectifFormSet = inlineformset_factory(Course, objectif, fields=('points',))
VideoFormSet = inlineformset_factory(Course, Video, fields=('__all__'))