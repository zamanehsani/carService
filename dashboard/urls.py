from django.urls import path
from dashboard import views


urlpatterns = [
    path('',views.IndexClass.as_view(),name='index'),
]
