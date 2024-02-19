from rest_framework import serializers
from django.contrib.auth.models import User
import os
from dashboard import models as dashboard_models

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
    class Meta:
        model = dashboard_models.Company
        fields = ['name', 'description', 'logo', 'phone', 'address']
        depth = 1

class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dashboard_models.Customers
        fields = ['name', 'phone', 'address', 'description', 'price', 'image', 'date', 'company']
        depth = 1