from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from services.models import Service
from django.db.models import Count


def home(request):
    top_services = Service.objects.annotate(num_requests=Count('servicerequest')).order_by('-num_requests')[:5]
    return render(request, "main/home.html", {'top_services': top_services})

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")

def company_list(request):
    return render(request, 'users/list.html')