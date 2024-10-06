import os
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crop_plan', views.crop_plan, name='crop_plan'),
    path('market', views.market, name='market'),
    path('weather', views.weather, name='weather'),
    path('api/crops/', views.crop_list, name='crop-list'),
    path('api/districts/', views.district_list, name='district-list'),
    path('api/crop-details/', views.crop_details, name='crop-details'),
    path('api/sales-report/', views.sales_report, name='sales-report'),
    path('api/crops-desc/', views.crop_list_view, name='crop-desc'),
    path('get_weather_data/<str:district_name>/', views.get_weather_data, name='get_weather_data'),
]
