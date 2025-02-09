from django.urls import path
from .views import CustomAuthToken
from .views import *
from django.conf import settings
from django.conf.urls.static import static 
 
urlpatterns = [
    path('login-token', CustomAuthToken.as_view(), name='api_token_auth'), 
    path('allocate_driver_to_vehicle', allocate_driver_to_vehicle, name='admin_allocate_driver_to_vehicle'), 
    path('leave_driver_from_vehicle', leave_driver_from_vehicle, name='admin_leave_driver_from_vehicle'), 
 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

