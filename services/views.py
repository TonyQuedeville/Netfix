from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})

def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    user = request.user
    
    # Vérifiez s'il s'agit d'un utilisateur "All in One"
    is_all_in_one = user.company.field == 'All in One'
    
    # Créez une instance de formulaire avec la valeur par défaut
    form = CreateNewService(request.POST or None, initial={'field': user.company.field})
    
    if request.method == 'POST':
        # Si ce n'est pas un utilisateur "All in One", désactivez le champ "field"
        if not is_all_in_one:
            form.fields['field'].initial = user.company.field
            form.fields['field'].widget.attrs['disabled'] = 'disabled'
    
        if form.is_valid():
            # Lorsque is_valid() est appelée, Django exécute automatiquement toutes les méthodes clean_<field_name>
            # en locurence: clean_price_hour() dans forms.py
            
            service=form.save(commit=False)
            # Cette ligne crée une instance de l'objet "Service" en utilisant les données du formulaire (form). 
            # Cependant, la particularité ici est l'utilisation de commit=False. Cela signifie que le modèle "Service" 
            # n'est pas encore enregistré dans la base de données. L'objet "service" est créé en mémoire, 
            # mais il n'est pas encore persistant en base de données.
            service.company = user.company 
            # Vous récupérez l'entreprise associée à l'utilisateur connecté (request.user). Cela suppose que chaque utilisateur 
            # appartient à une entreprise, et cette ligne de code attribue cette entreprise à la variable company.
            service.save()
            # Enregistrement dans la table de la base de données "Service"
            
            
            # Redirigez l'utilisateur vers la page du service nouvellement créé ou une autre page appropriée
            return HttpResponseRedirect('/services/') 
    else:
        form = CreateNewService()
        if not is_all_in_one:
            form.fields['field'].initial = user.company.field
            form.fields['field'].widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'services/create_service.html', {'form': form})


# afficher une liste de services qui appartiennent à un domaine
def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = Service.objects.get(id=id)    
    user=request.user
    customer = Customer.objects.get(user=user)
    
    if request.method == 'POST': # 
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data  # Accédez aux données nettoyées
            
            # Créez une instance de ServiceRequest à partir des données du formulaire
            service_request = ServiceRequest(
                address=cleaned_data['address'],
                service_hours=cleaned_data['service_hours'],
                service=service,  # Associez le service
                customer=customer,  # Associez le client
            )
            
            # Calculez le prix total
            total_price = service.price_hour * form.cleaned_data['service_hours']
            service_request.total_price = total_price
            
            # Enregistrez le ServiceRequest en base de données
            service_request.save()
            
            return HttpResponseRedirect('/customer/' + user.username)
    else: # Affichage du formulaire vide à l'état initial
        form = RequestServiceForm()
        
    return render(request, 'services/request_service.html', {'form': form})
