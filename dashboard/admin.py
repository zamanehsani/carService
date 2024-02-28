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


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'invoice_number', 'date', 'image', 'price', 'description', 'company', 'user']
    list_display_links = ["name", 'invoice_number', 'date']
admin.site.register(models.Invoice, InvoiceAdmin)

class CustomersAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'description', 'price', 'image', 'date']
    list_display_links = ["name", 'phone', 'address']
admin.site.register(models.Customers, CustomersAdmin)

class OilChangeAdmin(admin.ModelAdmin):
    list_display = ['oil', 'amount', 'currentMilage', 'description', 'date', 'company','user','customer']
    list_display_links = ["oil", 'amount', 'date', 'company','user']
admin.site.register(models.OilChange, OilChangeAdmin)

 

class TintAdmin(admin.ModelAdmin):
    list_display = ['tintPercentage', 'tintedWindows', 'tintType','amount', 'description', 'date', 'company','user','customer']
    list_display_links = ["tintPercentage",'tintedWindows','tintType', 'amount', 'date', 'company','user']
admin.site.register(models.Tint, TintAdmin)

class TyreAdmin(admin.ModelAdmin):
    list_display = ['tyreType','tyreNumber','quantity', 'amount', 'description', 'date', 'company','user','customer']
    list_display_links = ["tyreType",'tyreNumber','quantity', 'amount', 'date', 'company','user']
admin.site.register(models.Tyre, TyreAdmin)

class BatteryAdmin(admin.ModelAdmin):
    list_display = ['name','size','amount', 'description', 'date', 'company','user','customer']
    list_display_links = ["name",'size', 'amount', 'date', 'company','user']
admin.site.register(models.Battery, BatteryAdmin)


class OtherServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'description', 'date', 'company','user','customer']
    list_display_links = ["name", 'amount', 'date', 'company','user']
admin.site.register(models.OtherService, OtherServiceAdmin)

