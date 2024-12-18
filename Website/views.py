from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def about_us(request):
    return render(request,"about_us.html")

def material_handling(request):
    return render(request,"material-handling.html")

def contact_us(request):
    return render(request,"contact.html")

def crushing_services(request):
    return render(request,"crushing-services.html")

def equipment(request):
    return render(request,"equipment.html")

def clients(request):
    return render(request,"clients.html")

def photo_gallery(request):
    return render(request,"photo_gallery.html")
