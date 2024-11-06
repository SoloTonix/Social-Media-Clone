from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from.models import UserProfile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'followers']
