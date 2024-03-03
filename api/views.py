from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from dashboard import models as dashboard_models
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from api import serializers as apiSerializers
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
import json

class CustomPagination(PageNumberPagination):
    """
    We are creating a custome pagination 
    to limit the query and more """
    page_size = 2  # Number of items per page
    page_size_query_param = 'page_size'  # Allows the client to override the page size
    max_page_size = 100  # Maximum page size to prevent abuse

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

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

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    

    def create(self, request, *args, **kwargs):
        # must have the company_id, user_id 
        customer_obj = dashboard_models.Customers.objects.create(
            name    = request.data.get('name'),
            phone   = request.data.get('phone'),
            address = request.data.get('address'),
            price   = float(request.data.get('total')),
            company_id  = int(request.data.get('company_id')),
            car_plate_number = request.data.get('car_plate_number'),
            car_model = request.data.get('car_model'),
            car_plate_source = request.data.get('car_plate_source'),
            user_id     = int(request.data.get('user_id')),
        )
        customer_obj.image = request.FILES.get('photo')
        customer_obj.save()

        if request.data.get('oilChangeService'):
            oil_obj = dashboard_models.OilChange.objects.create(
                oil = request.data.get('oil'),
                currentMilage = request.data.get('currentMilage'),
                customer = customer_obj,
                company_id = request.data.get('company_id'),
                user_id = request.data.get('user_id'),
                amount = request.data.get('oilAmount')
            )
            oil_obj.save()
        
        if request.data.get('batteryService'):
            battery_obj = dashboard_models.Battery.objects.create(
                name = request.data.get('batteryName'),
                size = request.data.get('batterySize'),
                amount = request.data.get('batteryAmount'),
                warrenty = request.data.get('warranty'),
                customer = customer_obj,
                company_id = request.data.get('company_id'),
                user_id = request.data.get('user_id')
            )
            battery_obj.save()

        if request.data.get('tintService'):
            tint_obj = dashboard_models.Tint.objects.create(
                tintedWindows = request.data.get('tintedWindows'),
                tintPercentage = request.data.get('tintPercentage'),
                tintType = request.data.get('tintType'),
                amount = request.data.get('tintAmount'),
                customer = customer_obj,
                company_id = request.data.get('company_id'),
                user_id = request.data.get('user_id')
            )
            tint_obj.save()
        
        if request.data.get('tyreService'):
            tyre_obj = dashboard_models.Tyre.objects.create(
                tyreType = request.data.get('tyreType'),
                tyreNumber = request.data.get('tyreNumber'),
                quantity = request.data.get('tyreQuantity'),
                amount = request.data.get('tyreAmount'),
                customer = customer_obj,
                company_id = request.data.get('company_id'),
                user_id = request.data.get('user_id')
            )
            tyre_obj.save()

        if request.data.get('otherService'):
            obj_json = json.loads(request.data.get('otherItems'))
            for item in obj_json:
                other_obj = dashboard_models.OtherService.objects.create(
                    name = item['name'],
                    amount = item['amount'],
                    customer = customer_obj,
                    company_id = request.data.get('company_id'),
                    user_id = request.data.get('user_id')
                )
                other_obj.save()
        return Response(status=status.HTTP_201_CREATED)
    
class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Invoice.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.InvoicesSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    

    def create(self, request, *args, **kwargs):
        # must have the company_id, user_id 
        obj = dashboard_models.Invoice.objects.create(
            invoice_number  = request.data.get('invoice_number'),
            supplier_number = request.data.get('supplier_number'),
            name    = request.data.get('name'),
            price   = float(request.data.get('price')),
            quantity    = request.data.get('quantity'),
            description = request.data.get('description'),
            company_id  = int(request.data.get('company_id')),
            user_id     = int(request.data.get('user_id')),
        )
        # after the instance is created, save image to get the company instance and user instance.
        obj.image = request.FILES.get('image')
        obj.save()

        return Response(status=status.HTTP_201_CREATED)



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

# a view to get the user based on the username passed via post request
class GetUser(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = apiSerializers.UserSerializer(user,context={'request': request})
        return Response(serializer.data)
    
# a view to get the company based on the username passed via post request
class GetCompany(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        print("user company: ", username)
        try:
            company = dashboard_models.Company.objects.get(admin__username=username)
        except dashboard_models.Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = apiSerializers.CompaniesSerializer(company,context={'request': request})
        return Response(serializer.data)
