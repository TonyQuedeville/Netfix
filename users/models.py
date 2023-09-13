from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth = models.DateField()
    USERNAME_FIELD = 'email'
    
    def create_user_with_password(self, username, email, password):
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        self.user = user
        self.save()
    
    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(
                                max_length=70, 
                                choices=(
                                            ('All in One', 'Tout en un'),
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
                                        ), blank=False, null=False)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    USERNAME_FIELD = 'email'
    
    def create_user_with_password(self, username, email, password):
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        self.user = user
        self.save()
        
    def get_context_data(self):
        context = {
            'user': self.user,
            'field': self.field,
            'rating': self.rating,
        }
        return context
    
    def get_field_url(self):
        return f"/services/{slugify(self.field)}/"

    def __str__(self):
        return str(self.user.username)

# Evaluation Company
class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user')
        
    def get_display_rating(self):
        return 6 - self.rating  # Inversion 5 <-> 1, 4 <-> 2      
