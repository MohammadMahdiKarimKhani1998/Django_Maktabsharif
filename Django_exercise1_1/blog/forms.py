from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, Form
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from blog.models import Comment

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(label=_('email'), help_text=_('a valid email for reset your password'))
    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}), required=True)
    # first_name = forms.CharField(label=_('first_name'))
    # last_name = forms.CharField(label=_('last_name'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), }

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


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), max_length=25)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Content'}), }

    # def save(self, user=None, post=None):
    #     comment = super(CommentForm, self).save(commit=False)
    #     if user and post:
    #         comment.author = user
    #         comment.post = post
    #     comment.save()
    #     return comment
