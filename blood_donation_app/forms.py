from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from blood_donation_app.models import User, Request


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            "username", 'first_name', 'last_name', 'email', "phone", "blood_group", "is_donor", 'password1',
            'password2',)


class RequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].widget = SelectDateWidget()

    class Meta:
        model = Request
        fields = ('required_blood_group', 'deadline')
