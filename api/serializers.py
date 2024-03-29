from rest_framework import serializers
from django.contrib.auth.models import User, Permission
import os
from dashboard import models as dashboard_models
from django.contrib.contenttypes.models import ContentType



class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class UserPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'name': {'write_only': True},
        }

    def create(self, validated_data):
        permission = Permission.objects.create(name=validated_data['name'])
        return permission

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    def validate_name(self, value):
        if Permission.objects.filter(name=value).exists():
            raise serializers.ValidationError('Permission already exists')
        return value

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = dashboard_models.User_profile
        fields = '__all__'  # Include all fields from the Profile model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True) 
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        depth = 1
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','username']
        extra_kwargs = {'password': {'write_only': True}}

class UsersProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dashboard_models.User_profile
        fields = [ 'profile', 'company', 'user','id']
        depth = 1

# this is for other serializers
class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','last_login', 'first_name', 'last_name','user_permissions','groups', 'date_joined']

class CompaniesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    admin = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Company
        fields = "__all__"
        depth = 1


class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    oilChangeService = serializers.SerializerMethodField(read_only=True)
    batteryService = serializers.SerializerMethodField(read_only=True)
    tintService = serializers.SerializerMethodField(read_only=True)
    tyreService = serializers.SerializerMethodField(read_only=True)
    otherService = serializers.SerializerMethodField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Customers
        fields = "__all__"
        depth = 1
    
    def get_oilChangeService(self, obj):
        oiChange =  obj.oilchange_set.all()
        serializer = OilChangeSer(oiChange, many=True)
        return serializer.data
    
    def get_batteryService(self, obj):
        batteries =  obj.battery_set.all()
        serializer = BatterySer(batteries, many=True)
        return serializer.data

    def get_tintService(self, obj):
        tint = obj.tint_set.all()
        serializer = TintSer(tint, many=True)
        return serializer.data
    
    def get_tyreService(self, obj):
        tyres = obj.tyre_set.all()
        serializer = TyreSer(tyres, many=True)
        return serializer.data
    
    def get_otherService(self, obj):
        other_services = obj.otherservice_set.all()
        serializer = OtherServiceSer(other_services, many=True)
        return serializer.data

    

class InvoicesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField() 
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Invoice
        fields = "__all__"
        depth = 1


class CustomerSer(serializers.ModelSerializer):
    class Meta:
        model = dashboard_models.Customers
        fields = "__all__"

class CompanySer(serializers.ModelSerializer):
    class Meta:
        model = dashboard_models.Company
        fields = "__all__"

class OilChangeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    customer = CustomerSer(read_only=True)
    company = CompanySer(read_only=True)
    class Meta:
        model = dashboard_models.OilChange
        fields = "__all__"
        depth = 1

class OilChangeSer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.OilChange
        fields ="__all__"
      
class BatterySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Battery
        fields = "__all__"
        depth = 1


class BatterySer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Battery
        fields = "__all__"


class TintSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField() 
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Tint
        fields = "__all__"
        depth = 1

class TintSer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Tint
        fields = "__all__"

class TyreSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Tyre
        fields = "__all__"
        depth = 1

class TyreSer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.Tyre
        fields = "__all__"

class OtherServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField() 
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.OtherService
        fields = "__all__"
        depth = 1

class OtherServiceSer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    user = UserSer(read_only=True)
    class Meta:
        model = dashboard_models.OtherService
        fields = "__all__"
