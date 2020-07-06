from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from blog.models import Series


class RegisterForm(UserCreationForm):
    password1   =   forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class':"form-control",
        'placeholder':"Enter Password"
    }))
    password2   =   forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class':"form-control",
        'placeholder':"Confirm Password"
    }))
    class Meta:
        model   =   User
        fields  =   ['username','email','gender','country','password1','password2']




class ProfileUpdate(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows':'6',
        'class': 'form-control',
        'placeholder':'Write a Short Bio'
    }))
    class Meta:
        model   =   User
        fields  =   ['bio']




class BioUpdate(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows':'6',
        'class': 'form-control',
        'placeholder':'Write a Short Bio'
    }))
    class Meta:
        model   =   User
        fields  =   ['bio',]


