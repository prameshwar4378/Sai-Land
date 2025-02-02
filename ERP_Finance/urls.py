from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='finance_dashboard'),
    path('vehicle_list/', views.vehicle_list, name='finance_vehicle_list'),
    path('vehicle_dashboard/<int:id>', views.vehicle_dashboard, name='finance_vehicle_dashboard'),
    path('create_other_dues/', views.create_other_dues, name='finance_create_other_dues'),
    path('update_other_dues/<int:id>', views.update_other_dues, name='finance_update_other_dues'),

    path('emi_list/', views.emi_list, name='finance_emi_list'),
    path('create_emi/', views.create_emi, name='finance_create_emi'),
    path('delete_emi/<int:id>', views.delete_emi, name='finance_delete_emi'),
    path('update_emi/<int:id>', views.update_emi, name='finance_update_emi'),

    path('emi_installments_list/<int:id>', views.emi_installments_list, name='finance_emi_installments_list'),

    path('emi_item_list/<int:id>', views.emi_item_list, name='finance_emi_item_list'),
    path('delete_emi_item/<int:id>', views.delete_emi_item, name='finance_delete_emi_item'),

    path('policy_list/', views.policy_list, name='finance_policy_list'),
    path('create_policy/', views.create_policy, name='finance_create_policy'),
    path('delete_policy/<int:id>', views.delete_policy, name='finance_delete_policy'),
    path('update_policy/<int:id>', views.update_policy, name='finance_update_policy'),

    path('reports_list/', views.reports_list, name='finance_reports_list'),

     
    path('insurance_bank_list/', views.insurance_bank_list, name='finance_insurance_bank_list'),
    path('insurance_bank_update/<int:id>', views.insurance_bank_update, name='finance_insurance_bank_update'),
    path('insurance_bank_delete/<int:id>', views.insurance_bank_delete, name='finance_insurance_bank_delete'),
    
    path('finance_bank_list/', views.finance_bank_list, name='finance_finance_bank_list'),
    path('finance_bank_update/<int:id>', views.finance_bank_update, name='finance_finance_bank_update'),
    path('finance_bank_delete/<int:id>', views.finance_bank_delete, name='finance_finance_bank_delete'),

    path('purchase_list/', views.purchase_list, name='finance_purchase_list'),
    path('purchase_item_list/<int:id>', views.purchase_item_list, name='finance_purchase_item_list'),
    path('update_purchase/<int:id>', views.update_purchase, name='finance_update_purchase')
]
