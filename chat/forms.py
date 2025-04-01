from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()  # Email field, not included by default in UserCreationForm
    image = forms.ImageField(required=False)  # Optional image field for profile picture

    class Meta:
        model = User  # The form is tied to the User model
        fields = ['username', 'email', 'password1', 'password2', 'image']  # Fields to include in the form
