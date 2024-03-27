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
from rest_framework import filters
from rest_framework.views import APIView




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
        queryset = dashboard_models.User.objects.all().order_by('-date_joined')
        return queryset

class UserUpdateAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        user = dashboard_models.User.objects.get(pk = request.data.get("user_id"))
        serializer = apiSerializers.UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            if request.FILES.get('photo'):
                user.user_profile.profile = request.FILES.get('photo')
                user.user_profile.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

    def create(self, request, *args, **kwargs):
        # must have the company_id, user_id 
        username    = request.data.get("username")
        first_name  = request.data.get("first_name")
        last_name   = request.data.get("last_name")
        email       = request.data.get("email")

        user_obj = User.objects.create(
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
            email       = email
        )
        user_obj.save()
        user_obj.set_password(request.data.get('password'))
        user_obj.save()

        company_obj = dashboard_models.Company.objects.get(pk = request.data.get("company_id"))
        if user_obj and company_obj:
            obj = dashboard_models.User_profile.objects.create(
                user = user_obj,
                company= company_obj
            )
            obj.save()
            # after the instance is created, save image to get the company instance and user instance.
            if request.FILES.get('profile'):
                obj.profile = request.FILES.get('profile')
                obj.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

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
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'address', 'description','price','date','car_plate_number','car_plate_source','car_model']

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
            description = request.data.get('description'),
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'invoice_number', 'quantity','supplier_name','supplier_number','date','price','description']

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
            supplier_name = request.data.get('supplier_name'),
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['description','amount','date','currentMilage','oil']
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    

class BatteryViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Battery.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.BatterySerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','description','amount','date','size','warrenty']
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    

class TintViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Tint.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.TintSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['description','amount','date','tintedWindows','tintPercentage','tintType']
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset

class TyreViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.Tyre.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.TyreSerializer
    pagination_class = CustomPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['description','amount','date','tyreType', 'tyreNumber', 'quantity']
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    

class OtherServiceViewSet(viewsets.ModelViewSet):
    queryset = dashboard_models.OtherService.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.OtherServiceSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','description','amount','date']
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    
class CompanyUsers(viewsets.ModelViewSet):
    queryset = dashboard_models.User_profile.objects.all().order_by('user')
    permission_classes = (AllowAny,)
    serializer_class = apiSerializers.UsersProfileSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the query parameter named 'filter_param' from the request
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__id=company)
        return queryset
    
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
        try:
            u = User.objects.get(username=username)
        except dashboard_models.Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = apiSerializers.CompaniesSerializer(u.user_profile.company,context={'request': request})
        return Response(serializer.data)
