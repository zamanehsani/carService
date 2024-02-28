from rest_framework import routers
from django.urls import path, include
from api import views as apiViews


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('user', apiViews.UserViewSet)
router.register('permission', apiViews.UserPermissionViewSet)
router.register('content-type', apiViews.ContentTypeViewSet)
router.register('profile', apiViews.UsersProfileViewSet)
router.register('companies', apiViews.CompaniesViewSet)
router.register('customers', apiViews.CustomersViewSet)
router.register('invoices', apiViews.InvoicesViewSet)
router.register('oil-change', apiViews.OilChangeViewSet)
router.register('battery', apiViews.BatteryViewSet)
router.register('tint', apiViews.TintViewSet)
router.register('tyre', apiViews.TyreViewSet)
router.register('other-service', apiViews.OtherServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]