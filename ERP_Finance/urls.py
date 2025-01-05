from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='finance_dashboard'),
    path('vehicle_list/', views.vehicle_list, name='finance_vehicle_list'),
    path('vehicle_dashboard/<int:id>', views.vehicle_dashboard, name='finance_vehicle_dashboard'),
    path('create_insurance_tax_due/', views.create_insurance_tax_due, name='finance_create_insurance_tax_due'),
    path('update_insurance_tax_due/<int:id>', views.update_insurance_tax_due, name='finance_update_insurance_tax_due'),

    path('emi_list/', views.emi_list, name='finance_emi_list'),
    path('create_emi/', views.create_emi, name='finance_create_emi'),
    path('delete_emi/<int:id>', views.delete_emi, name='finance_delete_emi'),
    path('update_emi/<int:id>', views.update_emi, name='finance_update_emi'),

    path('emi_item_list/<int:id>', views.emi_item_list, name='finance_emi_item_list'),
    path('delete_emi_item/<int:id>', views.delete_emi_item, name='finance_delete_emi_item'),

    path('policy_list/', views.policy_list, name='finance_policy_list'),
    path('create_policy/', views.create_policy, name='finance_create_policy'),
    path('delete_policy/<int:id>', views.delete_policy, name='finance_delete_policy'),
    path('update_policy/<int:id>', views.update_policy, name='finance_update_policy'),

    path('reports_list/', views.reports_list, name='finance_reports_list'),
]
