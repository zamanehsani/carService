from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os


def customer_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    company = instance.company.id 
    filename, ext = os.path.splitext(filename)  # Split the filename and extension
    filename = f"{timestamp}-{instance.id}{ext}"  # Add the extension back to the filename
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
    filename = f"{timestamp}{ext}"
    return f"{company}/{filename}"

def invoice_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    company = instance.company.id
    filename, ext = os.path.splitext(filename)
    filename = f"{timestamp}-{instance.id}{ext}"
    return f"{company}/{filename}"

class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=company_logo_path, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
         verbose_name = 'Company'
         verbose_name_plural = 'Companies'
         ordering = ['-name']

    def __str__(self):
        return str(self.pk)
    
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to=profile_file_path, null=True, blank=True)

    class Meta:
         verbose_name = 'User Profile'
         verbose_name_plural = 'User Profiles'
         ordering = ['-user']   
    def __str__(self):
        return self.user.username

class Customers(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to=customer_file_path, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank= True)
    user  = models.ForeignKey(User, null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
         verbose_name = 'Customer'
         verbose_name_plural = 'Customers'
         ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    

# make a model with name, invoice number, date, image, price, description
class Invoice(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    supplier_number = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=invoice_file_path, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User,null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)


class OilChange(models.Model):
    oil = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    currentMilage = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, null=True, blank = True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customers, null=True, blank = True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name = 'Oil Change'
        verbose_name_plural = 'Oil Changes'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    
class Tint(models.Model):
    tintedWindows = models.PositiveSmallIntegerField(null=True, blank=True)
    tintPercentage = models.PositiveSmallIntegerField(null=True, blank=True)
    tintType = models.CharField(max_length=1200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User,null=True, blank = True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customers,null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Tint'
        verbose_name_plural = 'Tints'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    
class Tyre(models.Model):
    tyreType = models.CharField(max_length=10, null=True, blank=True)
    tyreNumber = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, null=True, blank = True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customers, null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Tyre Change'
        verbose_name_plural = 'Tyre Changes'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    
class Battery(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    size = models.PositiveSmallIntegerField( null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warrenty= models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, null=True, blank = True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customers, null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    
class OtherService(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, null=True, blank = True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customers, null=True, blank = True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Other Service'
        verbose_name_plural = 'Other Services'
        ordering = ['-date']

    def __str__(self):
        return str(self.pk)
    
