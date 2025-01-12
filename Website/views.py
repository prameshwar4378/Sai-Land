from django.shortcuts import render
import threading
from ERP_Admin.models import Enquiry
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

# Create your views here.


def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print("name : ",name)
        print("mobile : ",mobile)
        print("email : ",email)
        print("subject : ",subject)
        print("message : ",message)

        if name and mobile and email and subject and message:
            # Save the enquiry in the database
            Enquiry.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                subject=subject,
                message=message
            )

            # Prepare email content
            email_subject = f"New Enquiry from : {name}"
            email_body = (
                f"Dear Team,\n\n"
                f"You have received a new enquiry from your website.\n\n"
                f"Details:\n"
                f"Subject: {subject}\n\n"
                f"Name: {name}\n"
                f"Mobile: {mobile}\n"
                f"Email: {email}\n"
                f"Message:\n"
                f"{message}\n\n"
                f"Regards,\n"
                f"Website Enquiry System"
            )

            # Configure the email
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['vitthalminde1@gmail.com'],  # Replace with the appropriate email address -- sales@dynaxcel.com
            )

            # Send the email in a separate thread to avoid blocking
            email_thread = threading.Thread(target=send_email_in_background, args=(email_message,))
            email_thread.start()

            # Success message to the user
            messages.success(request, "Your enquiry has been submitted successfully.")
        else:
            messages.error(request, "All fields are required")

        return redirect('/')

    return render(request, "index.html")



def about_us(request):
    return render(request,"about_us.html")

def material_handling(request):
    return render(request,"material-handling.html")


def send_email_in_background(email_message):
    try:
        email_message.send()
    except Exception as e:
        print(f"Error sending email: {e}")



def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print("name : ",name)
        print("mobile : ",mobile)
        print("email : ",email)
        print("subject : ",subject)
        print("message : ",message)

        if name and mobile and email and subject and message:
            # Save the enquiry in the database
            Enquiry.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                subject=subject,
                message=message
            )

            # Prepare email content
            email_subject = f"New Enquiry from : {name}"
            email_body = (
                f"Dear Team,\n\n"
                f"You have received a new enquiry from your website.\n\n"
                f"Details:\n"
                f"Subject: {subject}\n\n"
                f"Name: {name}\n"
                f"Mobile: {mobile}\n"
                f"Email: {email}\n"
                f"Message:\n"
                f"{message}\n\n"
                f"Regards,\n"
                f"Website Enquiry System"
            )

            # Configure the email
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['vitthalminde1@gmail.com'],  # Replace with the appropriate email address -- sales@dynaxcel.com
            )

            # Send the email in a separate thread to avoid blocking
            email_thread = threading.Thread(target=send_email_in_background, args=(email_message,))
            email_thread.start()

            # Success message to the user
            messages.success(request, "Your enquiry has been submitted successfully.")
        else:
            messages.error(request, "All fields are required")

        return redirect('/web/contact')

    return render(request, "contact.html")



def crushing_services(request):
    return render(request,"crushing-services.html")

def equipment(request):
    return render(request,"equipment.html")

def clients(request):
    return render(request,"clients.html")

def photo_gallery(request):
    return render(request,"photo_gallery.html")
