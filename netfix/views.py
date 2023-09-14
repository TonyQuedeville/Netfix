from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from utils.age_calculator import calculate_age
from users.models import User, Company, Customer, CompanyReview
from users.forms import CompanyReviewForm
from services.models import Service, ServiceRequest
from django.db.models import Avg


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
    company = get_object_or_404(Company, user__username=name)
    # user__username=name signifie que nous voulons filtrer les entreprises en fonction du nom 
    # d'utilisateur de leur propriétaire, où name est la valeur que nous passons en tant que 
    # paramètre à la vue.
    services = Service.objects.filter(company=company).order_by("-date")
    
    existing_review = None
    form = None
    
    if request.user.is_authenticated and request.user.is_customer and request.user.id != company.user_id: # Empeche l'auto évaluation et l'evaluation entre entreprises
        existing_review = CompanyReview.objects.filter(user=request.user, company=company).first()
        
        if request.method == 'POST':
                form = CompanyReviewForm(request.POST, instance=existing_review)
                if form.is_valid():
                    rating = form.save(commit=False)
                    rating.rating = 6 - rating.rating  # Inversion 5 <-> 1, 4 <-> 2, etc.
                    rating.user = request.user
                    rating.company = company
                    rating.save()
                    
                    calculate_company_rating(company)
        # else:
        #     form = CompanyReviewForm()
    else:
        form = CompanyReviewForm(instance=existing_review)

    context = {
        'user': company.user,
        'services': services,
        'rating': company.rating,
        'form': form,
        'company': company,
    }
    
    return render(request, 'users/profile.html', context)


def calculate_company_rating(company):
    print("calculate_company_rating !")
    # Récupérez toutes les évaluations associées à l'entreprise
    company_reviews = CompanyReview.objects.filter(company=company)
    
    # Calculez la note moyenne à partir de ces évaluations
    company_rating = company_reviews.aggregate(Avg('rating'))['rating__avg']
    print("moyenne eval",company, ":", company_reviews)
    
    # Mettez à jour la note de l'entreprise
    company.rating = company_rating
    company.save()