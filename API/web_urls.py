from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework.routers import DefaultRouter
from .web_api_views import *
from .android_api_views import *

  
urlpatterns = [ 
    # WEB APIS
    path('allocations', allocate_driver_list_create, name='api-allocate-driver-list-create-web'),
    path('allocations/<int:pk>', allocate_driver_detail, name='api-allocate-driver-detail-web'),

    path('breakdowns', breakdown_list_create, name='api-breakdown-list-create'),
    path('breakdowns/<int:pk>', breakdown_detail, name='api-breakdown-detail'),

    path('fuel_records', fuel_record_list_create, name='api-fuel-record-list-create'),
    path('fuel_records/<int:pk>', fuel_record_detail, name='api-fuel-record-detail'),

    path('breakdown_types', breakdown_type_list_create, name='api-breakdown-type-list-create'),
    path('breakdown_types/<int:pk>', breakdown_type_detail, name='api-breakdown-type-detail'),
 
    path('get_drivers', get_drivers, name='api-get-drivers'),
    path('get_vehicles', get_vehicles, name='api-get-vehicles'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
