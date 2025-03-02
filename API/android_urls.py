from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework.routers import DefaultRouter
from .web_api_views import *
from .android_api_views import *

  
urlpatterns = [
    path('login', login, name='api_login'), 
    path('get_vehicle_numbers', get_vehicle_numbers, name='api_get_vehicle_numbers'), 
    path('get_vehicle_details', get_vehicle_details, name='api_get_vehicle_details'), 

    path('allocate_driver_to_vehicle', allocate_driver_to_vehicle, name='api_allocate_driver_to_vehicle'), 
    path('leave_driver_from_vehicle', leave_driver_from_vehicle, name='api_leave_driver_from_vehicle'), 

    path('get_breakdown_type', get_breakdown_type, name='api_get_breakdown_type'), 
    path('create_breakdown', create_breakdown, name='api_create_breakdown'), 

    path('get_driver_allocation_history', get_driver_allocation_history, name='api_get_driver_allocation_history'), 

    path('get_vehicle_or_fuel_details', get_vehicle_or_fuel_details, name='api_get_vehicle_or_fuel_details'), 
    path('create_fuel_record', create_fuel_record, name='api_create_fuel_record'), 
    path('get_last_fuel_record', get_last_fuel_record, name='api_get_last_fuel_record'), 
    path('get_fuel_history', get_fuel_history, name='api_get_fuel_history'), 
  
    path('get_breakdown_list_for_workshop', get_breakdown_list_for_workshop, name='api_get_breakdown_list_for_workshop'),
    path('get_breakdown_details_for_workshop/<int:id>', get_breakdown_details_for_workshop, name='api_get_breakdown_details_for_workshop'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
