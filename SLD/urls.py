"""
URL configuration for SLD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Website import views as WebView 
from Website import urls as WebUrls
from ERP_Admin import urls as ERP_Admin_Urls
from ERP_Account import urls as ERP_Account_Urls
from ERP_Workshop import urls as ERP_Workshop_Urls
from ERP_Admin import views as ERP_Admin_View
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('default-admin/', admin.site.urls),
    path('', WebView.index, name="index"), 
    path('web/', include(WebUrls)), 
    path('admin/', include(ERP_Admin_Urls)),  
    path('account/', include(ERP_Account_Urls)),  
    path('workshop/', include(ERP_Workshop_Urls)),

    path('login/', ERP_Admin_View.login, name="login"), 
    path('logout/', ERP_Admin_View.logout, name="logout"),  
    path('delete_user/<int:id>', ERP_Admin_View.delete_user, name="delete_user"),  

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
