from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth = models.DateField()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=70, choices=(('Air Conditioner', 'Climatisation'),
                                                 ('All in One', 'Tout en un'),
                                                 ('Carpentry', 'Menuiserie'),
                                                 ('Electricity', 'Électricité'),
                                                 ('Gardening', 'Jardinage'),
                                                 ('Home Machines', 'Appareils ménagers'),
                                                 ('House Keeping', 'Entretien ménager'),
                                                 ('Interior Design', 'Design intérieur'),
                                                 ('Locks', 'Serrures'),
                                                 ('Painting', 'Peinture'),
                                                 ('Plumbing', 'Plomberie'),
                                                 ('Water Heaters', 'Chauffe-eau')), blank=False, null=False)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username
