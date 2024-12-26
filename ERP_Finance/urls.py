from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='finance_dashboard'),
    path('emi_list/', views.emi_list, name='finance_emi_list'),

    path('policy_list/', views.policy_list, name='finance_policy_list'),
    path('create_policy/', views.create_policy, name='finance_create_policy'),
    path('delete_policy/<int:id>', views.delete_policy, name='finance_delete_policy'),

    path('reports_list/', views.reports_list, name='finance_reports_list'),
]
