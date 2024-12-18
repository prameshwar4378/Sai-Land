from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "account_dashboard.html")

def payment_tracking(request):
    return render(request, "account_payment_tracking.html")

def renewal_management(request):
    return render(request, "account_renewal_management.html")

def reports(request):
    return render(request, "account_reports.html")