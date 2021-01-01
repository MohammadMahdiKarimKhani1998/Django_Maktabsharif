from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, Form
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from blog.models import Comment

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(label=_('email'), help_text=_('a valid email for reset your password'))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Password confirmation'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    # first_name = forms.CharField(label=_('first_name'))
    # last_name = forms.CharField(label=_('last_name'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), }


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
