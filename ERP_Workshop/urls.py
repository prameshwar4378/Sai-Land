from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('dashboard/', views.dashboard, name='workshop_dashboard'),
    path('breakdown-alerts/', views.breakdown_alerts, name='workshop_breakdown_alerts'),

    path('job_card_list/', views.job_card_list, name='workshop_job_card_list'),
    path('create_job_card/', views.create_job_card, name='workshop_create_job_card'),
    path('update_job_card/<int:id>', views.update_job_card, name='workshop_update_job_card'),
    path('delete_job_card/<int:id>', views.delete_job_card, name='workshop_delete_job_card'),
    path('job_card_item_list/<int:id>', views.job_card_item_list, name='workshop_job_card_item_list'),
    path('delete_job_card_item/<int:id>', views.delete_job_card_item, name='workshop_delete_job_card_item'),
    path('close_job_card/', views.close_job_card, name='workshop_close_job_card'),
    path('print_job_card/<int:id>', views.print_job_card, name='workshop_print_job_card'),

    path('maintenance-logs/', views.maintenance_logs, name='workshop_maintenance_logs'),
    path('maintenance-schedule/', views.maintenance_schedule, name='workshop_maintenance_schedule'),

    path('product-list/', views.product_list, name='workshop_product_list'),
    path('create-product/', views.create_product, name='workshop_create_product'),
    path('update_product/<int:id>', views.update_product, name='workshop_update_product'),
    path('import-product/', views.import_products, name='workshop_import_products'),
    path('delete-product/<int:id>', views.delete_product, name='workshop_delete_product'),

    path('purchase-list/', views.purchase_list, name='workshop_purchase_list'),
    path('create-purchase/', views.create_purchase, name='workshop_create_purchase'),
    path('update_purchase/<int:id>', views.update_purchase, name='workshop_update_purchase'),
    path('delete-purchase/<int:id>', views.delete_purchase, name='workshop_delete_purchase'),

    path('get_product_details/', views.get_product_details, name='workshop_get_product_details'),
    path('delete_purchase_item/<int:id>', views.delete_purchase_item, name='workshop_delete_purchase_item'),
    path('purchase-item-list/<int:id>', views.purchase_item_list, name='workshop_purchase_item_list'),

    path('reports/', views.reports, name='workshop_reports'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

