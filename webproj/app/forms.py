from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateClientForm(UserCreationForm):
    first_name = forms.CharField( max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 =forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 =forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

