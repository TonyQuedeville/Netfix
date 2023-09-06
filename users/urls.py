from django.urls import path
from django.contrib.auth import views

from .forms import UserLoginForm
from django.contrib.auth import views as auth_views
from . import views as v, forms as f

urlpatterns = [
    path('users/register/', v.register, name='register'),
    path('users/login/', v.LoginUserView, name='login_user'),
    path('register/company/', v.CompanySignUpView.as_view(), name='register_company'),
    path('register/customer/', v.CustomerSignUpView.as_view(), name='register_customer'),
]
