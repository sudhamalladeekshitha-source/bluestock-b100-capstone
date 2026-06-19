from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('companies/', views.company_list, name='company-list'),
    path('companies/<str:symbol>/', views.company_detail,
         name='company-detail'),
    path('sectors/', views.sector_view, name='sectors'),
]