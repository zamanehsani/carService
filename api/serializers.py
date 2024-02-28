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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    

class UsersProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dashboard_models.User_profile
        fields = [ 'profile', 'company', 'user']
        depth = 1

class CompaniesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Company
        fields = "__all__"
        depth = 1

class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Customers
        # fields = ['name', 'phone', 'address', 'description', 'price', 'image', 'date', 'company']
        fields = "__all__"
        depth = 1

class InvoicesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Invoice
        fields = "__all__"
        depth = 1


class OilChangeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.OilChange
        fields = "__all__"
        depth = 1

class BatterySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Battery
        fields = "__all__"
        depth = 1

class TintSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Tint
        fields = "__all__"
        depth = 1

class TyreSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.Tyre
        fields = "__all__"
        depth = 1

class OtherServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()  # Explicitly include the id field
    class Meta:
        model = dashboard_models.OtherService
        fields = "__all__"
        depth = 1