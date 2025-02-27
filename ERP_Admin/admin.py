# from django.contrib import admin
# from .models import *
# # Register your models here.
 
# admin.site.register(Product)
# admin.site.register(Finance_Bank)
# admin.site.register(Insurance_Bank)
# admin.site.register(BreakdownType)
# admin.site.register(Breakdown)
# admin.site.register(AllocateDriverToVehicle)
# admin.site.register(FuelRecord)

from django.contrib import admin
from django.apps import apps

# Get all models in the current app
app = apps.get_app_config('ERP_Admin')  # replace 'your_app_name' with your actual app name
for model in app.get_models():
    admin.site.register(model)
