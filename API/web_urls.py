from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework.routers import DefaultRouter
from .web_api_views import *
from .android_api_views import *

  
urlpatterns = [ 
    # WEB APIS
    path('allocations', allocate_driver_list_create, name='allocate-driver-list-create-web'),
    path('allocations/<int:pk>', allocate_driver_detail, name='allocate-driver-detail-web'),

    path('breakdowns', breakdown_list_create, name='breakdown-list-create'),
    path('breakdowns/<int:pk>', breakdown_detail, name='breakdown-detail'),

    path('fuel_records', fuel_record_list_create, name='fuel-record-list-create'),
    path('fuel_records/<int:pk>', fuel_record_detail, name='fuel-record-detail'),

    path('breakdown_types', breakdown_type_list_create, name='breakdown-type-list-create'),
    path('breakdown_types/<int:pk>', breakdown_type_detail, name='breakdown-type-detail'),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
