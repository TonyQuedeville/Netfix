from django.contrib import admin

from .models import User, Customer, Company, CompanyReview


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("user", "field", "rating")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "birth")
    

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "company", "comment", "rating", "date")
