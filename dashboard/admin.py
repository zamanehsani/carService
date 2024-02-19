from django.contrib import admin
from dashboard import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Permission)
admin.site.register(ContentType)

class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'profile']
    # list_filter = ['vote_date', 'last_update', 'your_vote']
    list_display_links = ["user",'company', 'profile']
admin.site.register(models.User_profile, UserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'logo','description']
    list_display_links = ["name", 'phone', 'address']
admin.site.register(models.Company, CompanyAdmin)

class CustomersAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'description', 'price', 'image', 'date', 'company']
    list_display_links = ["name", 'phone', 'address']
admin.site.register(models.Customers, CustomersAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'invoice_number', 'date', 'image', 'price', 'description', 'company', 'user']
    list_display_links = ["name", 'invoice_number', 'date']
admin.site.register(models.Invoice, InvoiceAdmin)