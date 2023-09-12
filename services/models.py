from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer

class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    choices = (
        # ('All in One', 'Tout en un'),
        ('Air Conditioner', 'Climatisation'),
        ('Carpentry', 'Menuiserie'),
        ('Electricity', 'Électricité'),
        ('Gardening', 'Jardinage'),
        ('Home Machines', 'Appareils ménagers'),
        ('House Keeping', 'Entretien ménager'),
        ('Interior Design', 'Design intérieur'),
        ('Locks', 'Serrures'),
        ('Painting', 'Peinture'),
        ('Plumbing', 'Plomberie'),
        ('Water Heaters', 'Chauffe-eau')
    )
    field = models.CharField(max_length=30, blank=False, null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, default='', blank=True) 
    service_hours = models.DecimalField(decimal_places=2, max_digits=100)
    total_price = models.DecimalField(decimal_places=2, max_digits=100)

    def __str__(self):
        return f"Service Request ID: {self.id} - Customer: {self.customer.user.username} - Service: {self.service.name}"
