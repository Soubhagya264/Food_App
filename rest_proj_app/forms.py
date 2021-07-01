from django import forms
from rest_proj_app.models import Contact
from rest_proj_app.models import Myadm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Contactform(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"
class CreateUserForm(UserCreationForm):
        class Meta:
            model=User
            fields=['username','email','password1','password2']
class Itemform(forms.ModelForm):
    class Meta:
        model=Myadm
        fields=['name','price','image']
