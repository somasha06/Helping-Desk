"""
URL configuration for Techsupport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from helpdesk.views import *
from django.conf import settings
from django.conf.urls.static import static
from helpdesk.adminview import *
from helpdesk.userview import *

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path("auth/",include("django.contrib.auth.urls")),

    path("admin/",admindashboard,name="admindashboard"),
    path("admin/manageusers/",manageusers,name="manageusers"),
    path("admin/managetickets/",managetickets,name="managetickets"),
    path("admin/viewticket/",viewticket,name="viewticket"),
    path("admin/reports/",reports,name="reports"),
    path("admin/settings/",adminsettings,name="adminsettings"),
    path("admin/manageagents/",manageagents,name="manageagents"),


    path("user/",userdashboard,name="userdashboard"),
    path("user/userticket/",usertickets,name="usertickets"),
    path("user/userticketdetail/<int:id>/",userticketdetail,name="userticketdetail"),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
