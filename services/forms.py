from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator
from users.models import Company
from .models import Service


class CreateNewService(forms.ModelForm):
    name = forms.CharField(max_length=40,  label='Service Name', 
                            widget=forms.TextInput(attrs={'placeholder': 'Enter Service Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Description'}), label='Description')
    price_hour = forms.DecimalField(decimal_places=2, max_digits=5, 
                                    validators=[MinValueValidator(Decimal('0.00'))], 
                                    widget=forms.NumberInput(attrs={'placeholder': 'Enter Price per Hour', 'id': 'hour-input', 'step': '0.05'}),
                                    label='Price per Hour',
                                    initial='0.00')
    
    field = forms.ChoiceField(
        required=True, 
        label='Field', 
        help_text='Select the field to which this service belongs.',
    )
    
    def __init__(self, *args, ** kwargs):
        initial_field = kwargs.get('initial', {})
        # field = initial_field.get('field', None)
        
        user = kwargs.pop('user', None)        
        
        super(CreateNewService, self).__init__(*args, **kwargs)
        
        # Choix par defaut
        initial_field = user.company.field
        
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        
        # Méthode d'ajout des choix du champ field en dynamique
        field_choices = []
        
        if user.company and user.company.field == 'All in One':
            field_choices = [
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
            ]
        else:
            field_choices = [(initial_field, initial_field)] if initial_field else []

        self.fields['field'].choices = field_choices
        self.fields['field'].initial = initial_field
    
    def clean_price_hour(self):
        price_hour = self.cleaned_data.get('price_hour')
        if price_hour <= Decimal('0.00'):
            raise forms.ValidationError("Price per hour must be greater than 0.")
        return price_hour
    
    class Meta:
        model = Service  # Le modèle associé à ce formulaire
        fields = ['field', 'name', 'description', 'price_hour']


class RequestServiceForm(forms.ModelForm):
    address = forms.CharField(max_length=100,  label='Address', 
                        widget=forms.TextInput(attrs={'placeholder': 'Enter Address'}))
    service_hours = forms.DecimalField(decimal_places=2, max_digits=5, 
                                    validators=[MinValueValidator(Decimal('0.25'))], 
                                    widget=forms.NumberInput(attrs={'placeholder': 'Enter Service Hours', 'id': 'hour-input', 'step': '0.25'}),
                                    label='Service Hours',
                                    initial='0.25')
    
    class Meta:
        model = Service  # Le modèle associé à ce formulaire
        fields = ['address', 'service_hours']
