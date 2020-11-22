from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models import  *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateClientForm(UserChangeForm):
    first_name = forms.CharField( max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UpdatePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = {'old_password', 'new_password1', 'new_password2'}



class PurchaseForm(forms.Form):
    '''
    These two fields of this form correspond to the form that will be used to complete a purchase( if there are no errors in the process of completion)
    '''
    productid=forms.IntegerField()
    paymenttype=forms.IntegerField()

class FavoritesForm(forms.Form):
    productid =forms.BooleanField(required=False,initial=False);



class ReviewForm(forms.Form):
    rating = forms.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0) ],
            help_text='Rate this app in a scale of 1 to 5',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    text = forms.CharField(max_length=50,help_text='Describe your experience!',widget=forms.TextInput(attrs={'class': 'form-control input-sm'}))



class EditProductForm(forms.Form):
    #this attribute will be hidden, only use to know what in view what product we are editing
    prod=forms.IntegerField()
    name = forms.CharField(max_length=50)
    icon=forms.URLField()
    description=forms.CharField(max_length=50)

    # nao sei porque esta a dar redirect no form
    #category = forms.ModelChoiceField(queryset=Category.objects.all())
    #developer = forms.ModelChoiceField(queryset=Developer.objects.all())

