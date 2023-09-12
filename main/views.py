from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from users.models import Company


def home(request):
    return render(request, "main/home.html", {})

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")

def company_list(request):
    return render(request, 'users/list.html')