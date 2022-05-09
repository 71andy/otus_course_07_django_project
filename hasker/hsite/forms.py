from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = '__all__'
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'size': 60}),
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) < 10:
    #         raise ValidationError('Title must be at least 10 characters')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        # fields = '__all__'
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
        }

    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     print(f"cleaned text={data}")
    #     return data


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-input'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-input'}),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username (nickname)', 'class': 'form-input'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'}),
    )
    password1 = forms.CharField(
        label='Password',
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-input',
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-input',
                'data-toggle': 'password',
                'id': 'password',
                'name': 'password',
            }
        ),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Profile
        fields = ['avatar']
