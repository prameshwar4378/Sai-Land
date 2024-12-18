 
from django.urls import path
from .views import  *
urlpatterns = [
    path('about-us', about_us, name="website_about_us"),
    path('material-handling', material_handling, name="material_handling"),
    path('contact', contact_us, name="contact_us"),
    path('crushing-services', crushing_services, name="crushing_services"),
    path('equipment', equipment, name="equipment"),
    path('clients', clients, name="clients"),
    path('photo_gallery', photo_gallery, name="photo_gallery"),
]
