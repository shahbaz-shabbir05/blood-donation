from django import forms
from django.contrib.auth.forms import UserCreationForm

from blood_donation_app.models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            "username", 'first_name', 'last_name', 'email', "phone", "blood_group", "is_donor", 'password1',
            'password2',)
