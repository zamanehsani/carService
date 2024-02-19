from rest_framework import routers
from django.urls import path, include
from api import views as apiViews


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('user', apiViews.UserViewSet)
router.register('profile', apiViews.UsersProfileViewSet)
router.register('companies', apiViews.CompaniesViewSet)
router.register('customers', apiViews.CustomersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]