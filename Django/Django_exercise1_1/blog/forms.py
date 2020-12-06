from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=150)
    email = forms.EmailField(label=_('email'), help_text=_('a valid email for reset your password'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label=_('first_name'))
    last_name = forms.CharField(label=_('last_name'))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        try:
            User.objects.get(username=username)
            raise ValidationError(_('This username already exist'), code='invalid')
        except User.DoesNotExist:
            pass
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if len(password) < 8:
            raise ValidationError(_('password is too short!'), code='invalid')
        return password
