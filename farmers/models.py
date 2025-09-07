from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('agrovet', 'Agrovet'),
        ('farmer', 'Farmer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    must_reset_password = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Agrovet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agrovet_profile')
    business_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    registered_by = models.ForeignKey(Agrovet, on_delete=models.CASCADE, related_name='registered_farmers')
    farm_location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.farm_location}"
