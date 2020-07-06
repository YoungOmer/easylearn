from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label="Question", widget=forms.TextInput(attrs={
        'placeholder':"Enter your question here.",
        'class':'form-control'
    }))
    #body = forms.CharField(max_length=5000, widget=forms.Textarea, required=False)

    class Meta:
        model   =   Question
        fields  =   ['title', 'body']