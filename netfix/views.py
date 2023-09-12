from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from utils.age_calculator import calculate_age
from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})

def customer_profile(request, name):
    user = get_object_or_404(User, username=name)
    
    if user.is_customer:
        # L'utilisateur est un client
        customer = get_object_or_404(Customer, user=user)
        age = calculate_age(customer.birth)
        services_requested = ServiceRequest.objects.filter(customer_id=user.id).order_by('-request_date')[:5]
        
        context = {
            'user':  customer.user,
            'customer': customer,
            'user_age': age, 
            'birth': customer.birth,
            'services_requested': services_requested,
        }
        
        return render(request, 'users/profile.html', context)
    else:        
        raise Http404("User type not recognized")


def company_profile(request, name):
    user = get_object_or_404(User, username=name)
    
    if user.is_company:
        # L'utilisateur est une entreprise
        company = get_object_or_404(Company, user=user)
        services = Service.objects.filter(company=company).order_by("-date")
        
        context = {
            'user': company.user,
            'services': services,
            'rating': company.rating,
        }
        
        return render(request, 'users/profile.html', context)
    else:
        raise Http404("User type not recognized")
