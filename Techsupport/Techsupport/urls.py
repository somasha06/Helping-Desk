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
from helpdesk.staffview import *

urlpatterns = [
    path('superadmin/', admin.site.urls),

    # login
    path('', home, name='home'),
    path('customlogin/', customlogin, name='customlogin'),
    path('getlogout/', getlogout, name='getlogout'),
    path('signupuser', signupuser, name='signupuser'),
    # path('signupstaff', signupstaff, name='signupstaff'),
    # path("auth/",include("django.contrib.auth.urls")),

    # admin
    path("admin/",admindashboard,name="admindashboard"),
    path("admin/manageusers/",manageusers,name="manageusers"),
    path("admin/managetickets/",managetickets,name="managetickets"),
    path("admin/adminview/<int:id>",adminview,name="adminview"),
    path("admin/reports/",reports,name="reports"),
    path("admin/settings/",adminsettings,name="adminsettings"),
    path("admin/user/",manageusers,name="manageusers"),
    path("admin/managestaff/",managestaff,name="managestaff"),
    path("admin/createstaff/", createstaff, name="createstaff"),
    path("adminhome", adminhome,name="adminhome"),
    path("admin/removestaff/<int:id>/",removestaff,name="removestaff"),
    # path("admin/editstaffdetail/<int:id>/",editstaffdetail,name="editstaffdetail"),


    # user
    path("userhome/user/",userdashboard,name="userdashboard"),
    path("user/userticket/",usertickets,name="usertickets"),
    path("user/userticketdetail/<int:id>/",userticketdetail,name="userticketdetail"),
    path("staffdashboard/",staffdashboard, name="staffdashboard"),
    path("userhome", userhome,name="userhome"),


    #staff
    path("staffhome/",staffhome,name="staffhome"),
    path("staffhome/staff/",staffdashboard,name="staffdashboard"),
    path("staffmanageticket/",staffmanagetickets,name="staffmanagetickets"),
    path("staffmanageticket/<int:id>",staffviewdetail,name="staffviewdetail"),
    path("taketicket/<int:id>",taketicket,name="taketicket"),
    path("closeticket/<int:id>/",closeticket,name="closeticket"),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
