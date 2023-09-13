from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import User, CompanyReview

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
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),
        label='User name'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Mot de passe'  # Définir l'intitulé personnalisé ici
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirmez le mot de passe'  # Définir l'intitulé personnalisé ici
    )
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Enter Date of Birth'}),
        label='Date de Naissance'  # Définir l'intitulé personnalisé ici
    )
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username','email', 'date_of_birth', 'password1', 'password2')

# formulaire d'inscription entreprise
class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        label='Adresse Email'
    )
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter Compagny name'}),
        label='Compagny name'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Mot de passe'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirmez le mot de passe'
    )
    field = forms.ChoiceField(
        choices=(
            ('All in One', 'Tout en un'),
            ('Air Conditioner', 'Climatisation'),
            ('Carpentry', 'Menuiserie'),
            ('Electricity', 'Électricité'),
            ('Gardening', 'Jardinage'),
            ('Home Machines', 'Appareils ménagers'),
            ('House Keeping', 'Entretien ménager'),
            ('Interior Design', 'Design intérieur'),
            ('Locks', 'Serrures'),
            ('Painting', 'Peinture'),
            ('Plumbing', 'Plomberie'),
            ('Water Heaters', 'Chauffe-eau')
        ),
        label='Domaine'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'field')


# Formulaire de login
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    # email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        # self.fields['email'].widget.attrs['autocomplete'] = 'off'
        # self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
    
    
# Formulaire d'évaluation d'entreprise
class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['rating', 'comment']

    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
    )
    comment = forms.CharField(
        widget = forms.Textarea(attrs={'rows': 4}),
        required=False,
    )
