from django.contrib import admin
from dashboard import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
admin.site.register(Permission)
admin.site.register(ContentType)

class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'profile']
    # list_filter = ['vote_date', 'last_update', 'your_vote']
    list_display_links = ["user",'company', 'profile']
admin.site.register(models.User_profile, UserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'admin','phone', 'address', 'logo','description']
    list_display_links = ['id','admin', "name", 'phone', 'address']
admin.site.register(models.Company, CompanyAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'invoice_number', 'supplier_number', 'date', 'image', 'price', 'description', 'company', 'user']
    list_display_links = ['id', "name", 'invoice_number','supplier_number', 'date']
admin.site.register(models.Invoice, InvoiceAdmin)

class CustomersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'description', 'price', 'image', 'date']
    list_display_links = ['id', "name", 'phone', 'address']
admin.site.register(models.Customers, CustomersAdmin)

class OilChangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'oil', 'amount', 'currentMilage', 'description', 'date', 'company','user','customer']
    list_display_links = ['id', "oil", 'amount', 'date', 'company','user']
admin.site.register(models.OilChange, OilChangeAdmin)

class TintAdmin(admin.ModelAdmin):
    list_display = ['id', 'tintPercentage', 'tintedWindows', 'tintType','amount', 'description', 'date', 'company','user','customer']
    list_display_links = ['id', "tintPercentage",'tintedWindows','tintType', 'amount', 'date', 'company','user']
admin.site.register(models.Tint, TintAdmin)

class TyreAdmin(admin.ModelAdmin):
    list_display = ['id', 'tyreType','tyreNumber','quantity', 'amount', 'description', 'date', 'company','user','customer']
    list_display_links = ['id', "tyreType",'tyreNumber','quantity', 'amount', 'date', 'company','user']
admin.site.register(models.Tyre, TyreAdmin)

class BatteryAdmin(admin.ModelAdmin):
    list_display = ['id','name','size','amount','warrenty', 'description', 'date', 'company','user','customer']
    list_display_links = ['id',"name",'size', 'amount','warrenty', 'date', 'company','user']
admin.site.register(models.Battery, BatteryAdmin)

class OtherServiceAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'amount', 'description', 'date', 'company','user','customer']
    list_display_links = ['id',"name", 'amount', 'date', 'company','user']
admin.site.register(models.OtherService, OtherServiceAdmin)
