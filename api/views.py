from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from dashboard import models as dashboard_models
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from api import serializers as apiSerializers
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


class CustomPagination(PageNumberPagination):
    """
    We are creating a custome pagination 
    to limit the query and more """
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allows the client to override the page size
    max_page_size = 100  # Maximum page size to prevent abuse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.UserSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = dashboard_models.User.objects.all()
        return queryset
    
class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.ContentTypeSerializer()
    pagination_class = CustomPagination
    

class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.UserPermissionSerializer
    pagination_class = CustomPagination


class UsersProfileViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.User_profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.UsersProfileSerializer

class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Company.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.CompaniesSerializer
    pagination_class = CustomPagination

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Customers.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.CustomersSerializer
    pagination_class = CustomPagination

class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Invoice.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.InvoicesSerializer
    pagination_class = CustomPagination


class OilChangeViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.OilChange.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.OilChangeSerializer
    pagination_class = CustomPagination

class BatteryViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Battery.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.BatterySerializer
    pagination_class = CustomPagination

class TintViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Tint.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.TintSerializer
    pagination_class = CustomPagination

class TyreViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Tyre.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.TyreSerializer
    pagination_class = CustomPagination

class OtherServiceViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.OtherService.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.OtherServiceSerializer
    pagination_class = CustomPagination
