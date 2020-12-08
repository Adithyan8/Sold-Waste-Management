from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TUser

""" class UserRegisterForm(UserCreationForm,forms.ModelForm):
    email = forms.EmailField() #by default required-true

    class Meta:
        model = TUser
        fields = ['username', 'email', 'password1', 'password2','area','landmark','city','state','zipcode'] #password2 - Confirmation Password
 """
class UserRegisterForm(UserCreationForm):
    class Meta:
        fields = ["username", "email", "password1", "password2",'area','landmark','city','state','zipcode']
        model = TUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Full name"
        self.fields["email"].label = "Email address"

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() 

    class Meta:
        model = TUser
        fields = ['username', 'email','area','landmark','city','state','zipcode']