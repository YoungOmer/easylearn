from .models import Blog
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField



class BlogForm(forms.ModelForm):
    class Meta:
        model   =   Blog
        fields  =   ['title','content','category']


