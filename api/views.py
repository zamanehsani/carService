from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from dashboard import models as dashboard_models
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from api import serializers as apiSerializers
from django.contrib.auth.models import User


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
