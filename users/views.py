from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm, CompanyReviewForm
from .models import User, Company, Customer, CompanyReview
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db.models import Avg


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


@login_required
def submit_review(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    existing_review = CompanyReview.objects.filter(user=request.user, company=company).first()
    
    if request.user.id == company.user_id: # Empeche l'auto évaluation
        if request.method == 'POST':
            form = CompanyReviewForm(request.POST, instance=existing_review)
        else:
            form = CompanyReviewForm()

    return render(request, 'company/profile.html', {})

