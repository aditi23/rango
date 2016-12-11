from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from tango.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password','email']


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['interest']