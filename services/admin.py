from django.contrib import admin

from .models import Service, ServiceRequest


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price_hour", "field", "date", "company_id")
    
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "service", "request_date", "address", "service_hours", "total_price")
