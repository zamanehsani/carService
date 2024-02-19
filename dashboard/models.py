from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os


def customer_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    company = instance.company.id 
    filename, ext = os.path.splitext(filename)  # Split the filename and extension
    filename = f"{timestamp}-{instance.name}{ext}"  # Add the extension back to the filename
    return f"{company}/customers/{filename}"

def profile_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    company = instance.company.id
    filename, ext = os.path.splitext(filename)
    filename = f"{timestamp}-{instance.user.username}{ext}"
    return f"{company}/users/{filename}"

def company_logo_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    company = instance.id
    filename, ext = os.path.splitext(filename)
    filename = f"{timestamp}-{instance.name}{ext}"
    return f"{company}/{filename}"

class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=company_logo_path, null=True, blank=True)

    class Meta:
         verbose_name = 'Company'
         verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
    
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to=profile_file_path, null=True, blank=True)

    class Meta:
         verbose_name = 'User Profile'
         verbose_name_plural = 'User Profiles'
    def __str__(self):
        return self.user.username

class Customers(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to=customer_file_path, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
         verbose_name = 'Customer'
         verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name