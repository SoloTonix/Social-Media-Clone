from django import forms
from.models import *

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    class Meta:
        model = Post
        fields = ['body']

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    class Meta:
        model = Comment
        fields = ['body']