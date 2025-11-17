from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from .userform import RegisterForm


def home(r):
    return render(r, 'home.html')



# def signup(request):
#     if request.method == "POST":
#         username=request.POST.get("username")
#         pass1=request.POST.get("password1")
#         pass2=request.POST.get("password2")
#         role=request.POST.get("role")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists! Please choose another one.")
#             return redirect('signup')

#         if pass1 != pass2:
#             messages.error(request, "Passwords do not match! Please try again.")
#             return redirect('signup')
        
#         user=User.objects.create_user(username=username,password=pass1)
#         user.save()

#         obj=Userrole.objects.create(user=user,role=role)
#         obj.save()
#         # if pass1 == pass2:
                
#         #     user=User() 
#         #     user.username=username
#         #     user.set_password(pass1)
#         #     user.save()

#         #     obj=Userrole() 
#         #     obj.user=user
#         #     obj.role=role
#         #     obj.save()    

#         login_user(request,user) 

#         if obj.role == "admin":
#             return redirect('admindashboard')
#         else:
#             return redirect('userdashboard')
            
#     return render(request,'signup.html')

# def login(request):
#     if request.method == "POST":
#         username=request.POST.get("username")
#         password=request.POST.get("password")

#         user=authenticate(request,username=username,password=password)

#         if user is not None:
#             login_user(request,user) 

#             if user.userrole.role == "admin":
#                 return redirect('admindashboard')
#             else:
#                 return redirect('userdashboard')
            
#     return render(request,'login.html')
        


def signupuser(request):
    form=RegisterForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            user=form.save()
            Userrole.objects.create(account=user,role="user")
            return redirect("customlogin")
    return render(request,"registration/signup.html",{"form":form})

# def signupstaff(request):
#     if not request.user.is_authenticated or request.user.roleinfo.role != "admin":
#         return redirect("login")

#     form = RegisterForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             staff = form.save()
#             Userrole.objects.create(account=staff, role="staff")
#             return redirect("admindashboard")

#     return render(request, "registration/signup.html", {"form": form})


def customlogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            role=user.roleinfo.role
            # if user.is_superuser:
            #     return redirect('admindashboard')
            
            if role == "admin"or user.is_superuser:
                return redirect("adminhome")
            elif role == 'staff':
                return redirect('staffhome')
            else:
                return redirect("userhome")
            
    return render(request,"registration/login.html")


def getlogout(r):
    logout(r)
    return redirect("home")



        
    





