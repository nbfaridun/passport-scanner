from django import forms
from .models import Userposts

class UserImageForm(forms.ModelForm):
    class Meta:
        model = Userposts
        fields = ['image']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)