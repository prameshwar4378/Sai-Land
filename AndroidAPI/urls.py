from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static 
 
urlpatterns = [
    # path('login-token', CustomAuthToken.as_view(), name='api_token_auth'), 
    path('login', login, name='api_login'), 
    path('get_vehicle_details', get_vehicle_details, name='api_get_vehicle_details'), 
    path('allocate_driver_to_vehicle', allocate_driver_to_vehicle, name='api_allocate_driver_to_vehicle'), 
    path('leave_driver_from_vehicle', leave_driver_from_vehicle, name='api_leave_driver_from_vehicle'), 
    path('get_breakdown_type', get_breakdown_type, name='api_get_breakdown_type'), 
    path('create_breakdown', create_breakdown, name='api_create_breakdown'), 
    path('get_driver_allocation_history', get_driver_allocation_history, name='api_get_driver_allocation_history'), 

 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

