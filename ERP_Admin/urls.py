from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 

from .export import *
urlpatterns = [
    path('login-token', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('reload_all_caches/', views.reload_all_caches, name='admin_reload_all_caches'),

    path('notifications/', views.notifications, name='admin_notifications'),
    path('financial-management/', views.financial_management, name='admin_financial_management'),
    path('live-status/', views.live_status, name='admin_live_status'),

    path('job_card_list/', views.job_card_list, name='admin_job_card_list'),
    path('job_card_item_list/<int:id>', views.job_card_item_list, name='admin_job_card_item_list'),

    path('purchase_list/', views.purchase_list, name='admin_purchase_list'),
    path('purchase_item_list/<int:id>', views.purchase_item_list, name='admin_purchase_item_list'),
 
    path('product_list/', views.product_list, name='admin_product_list'),

    path('report/', views.report, name='admin_report'),

    path('user-management/', views.user_management, name='admin_user_management'),
    path('create-user/', views.create_user, name='admin_create_user'),
    path('update_user/<int:id>', views.update_user, name='admin_update_user'),

    path('drivers-list/', views.drivers_list, name='admin_drivers_list'),
    path('create-driver/', views.create_driver, name='admin_create_driver'),
    path('import_drivers/', views.import_drivers, name='admin_import_drivers'),
    path('update-driver/<int:id>', views.update_driver, name='admin_update_driver'),
    path('update_driver_password/<int:id>', views.update_driver_password, name='admin_update_driver_password'),
    path('delete-driver/<int:id>/', views.delete_driver, name='admin_delete_driver'),

    path('vehicle-list/', views.vehicle_list, name='admin_vehicle_list'),
    path('create_vehicle/', views.create_vehicle, name='admin_create_vehicle'),
    path('update_vehicle/<int:id>', views.update_vehicle, name='admin_update_vehicle'),
    path('import_vehicles/', views.import_vehicles, name='admin_import_vehicles'),
    path('delete_vehicle/<int:id>/', views.delete_vehicle, name='admin_delete_vehicle'),

    path('technician-list/', views.technician_list, name='admin_technician_list'),
    path('create-technician/', views.create_technician, name='admin_create_technician'),
    path('update_technician/<int:id>', views.update_technician, name='admin_update_technician'),
    path('delete-technician/<int:id>/', views.delete_technician, name='admin_delete_technician'),


    path('party-list/', views.party_list, name='admin_party_list'),
    path('create-party/', views.create_party, name='admin_create_party'),
    path('update_party/<int:id>/', views.update_party, name='admin_update_party'),
    path('delete-party/<int:id>/', views.delete_party, name='admin_delete_party'),

    path('vehicle-dashboard', views.vehicle_data , name="vehicle_data"),

    path('export_filtered_job_cards', export_filtered_job_cards , name="export_filtered_job_cards"),
    path('export_purchase_data', export_purchase_data , name="export_purchase_data"),
    path('export_product_data', export_product_data , name="export_product_data"),
    path('export_vehicle_data', export_vehicle_data , name="export_vehicle_data"),
    path('export_driver_data', export_driver_data , name="export_driver_data"),
    path('export_technician_data', export_technician_data , name="export_technician_data"),
    path('export_party_data', export_party_data , name="export_party_data"),
    path('export_policy_data', export_policy_data , name="export_policy_data"),
    path('export_emi_data', export_emi_data , name="export_emi_data"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

