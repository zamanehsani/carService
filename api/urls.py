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

user_view = apiViews.GetUser.as_view({'post': 'post'})
company_view = apiViews.GetCompany.as_view({'post': 'post'})

urlpatterns = [
    path('', include(router.urls)),
    path('get-user/', user_view, name='get-user'),
    path('user-update/', apiViews.UserUpdateAPIView.as_view(), name='user-update'),
    path('reset-password/', apiViews.UserResetPassword.as_view(), name='resetpassword'),
    path('company-users/', apiViews.CompanyUsers.as_view({'get': 'list'}), name='company-users'),
    path('get-company/', company_view, name='get-company'),
    path('set-user-permission/', apiViews.setUserPermission, name='set-user-permission'),
    path('expense-range/', apiViews.ExpenseRange, name='expense-range'),
    path('sales-range/', apiViews.SalesRange, name='sales-range'),
    path('balance-range/', apiViews.getBalanceRange, name='balance-range'),
]