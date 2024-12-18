# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='account_dashboard'),
    path('payment-tracking/', views.payment_tracking, name='account_payment_tracking'),
    path('renewal-management/', views.renewal_management, name='account_renewal_management'),
    path('reports/', views.reports, name='account_reports'),
]
