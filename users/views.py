from cmath import log
from distutils.log import Log
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.decorators.csrf import csrf_protect

def register(request):
    return render(request, 'users/register.html')

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_customer = 1
        user.is_company = 0
        user.set_password(form.cleaned_data["password1"])
        user.save() # Sauvegarde en BDD dans la table User
        customer = Customer.objects.create(user=user, birth=form.cleaned_data["date_of_birth"])
        customer.save() # Sauvegarde en BDD dans la table Customer
        
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_customer = 0
        user.is_company = 1
        user.set_password(form.cleaned_data["password1"])
        user.save() # Sauvegarde en BDD dans la table User
        company = Company.objects.create(user=user, field=form.cleaned_data.get('field'), rating=0)  # Créez un objet Company associé
        company.save() # Sauvegarde en BDD dans la table Compagny
        
        login(self.request, user)
        return redirect('/')


@csrf_protect
def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # user = authenticate(request, email=email, password=password)
            print("authenticate:", user)
            print({user.is_customer})
            if user is not None:
                login(request, user)
                # Redirection en fonction des valeurs is_customer et is_company
                request.session['user_username'] = user.username
                if user.is_customer:
                    request.session['user_type'] = 'customer' 
                    return redirect(f'/customer/{user.username}')
                elif user.is_company:
                    request.session['user_type'] = 'company'
                    return redirect(f'/company/{user.username}')
                else:
                    # Gestion des cas où ni client ni compagnie
                    return redirect('/')
        else:
            messages.error(request, 'Adresse mail ou mot de passe erroné !') 
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})
