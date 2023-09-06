from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User, Company, Customer

# widget personnalisée pour les champs de date
class DateInput(forms.DateInput):
    input_type = 'date'

# vérifie si l'adresse e-mail existe déjà
def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")

# formulaire d'inscription client
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        label='Adresse Email'  # Définir l'intitulé personnalisé ici
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Mot de passe'  # Définir l'intitulé personnalisé ici
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirmez le mot de passe'  # Définir l'intitulé personnalisé ici
    )
    birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Enter Date of Birth'}),
        label='Date de Naissance'  # Définir l'intitulé personnalisé ici
    )
    class Meta:
        model = Customer
        fields =  ('birth',)

# formulaire d'inscription entreprise
class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        label='Adresse Email'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Mot de passe'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirmez le mot de passe'
    )
    field = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Field'}),
        label='Domaine'
    )
    
    class Meta:
        model = Company
        fields = ('field', 'rating')

# formulaire de login
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
