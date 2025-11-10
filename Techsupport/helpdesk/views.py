from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login as login_user,logout as logout_user
from django.contrib.auth.models import User
from .models import Userrole
from django.contrib import messages



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
        


def signup(r):
    form=UserCreationForm(r.POST or None)
    if r.method=="POST":
        if form.is_valid():
            user=form.save()
            Userrole.objects.create(user=user,role="user")
            return redirect("login")
    return render(r,"registration/signup.html",{"form":form})


def login(r):
    form=AuthenticationForm(r, data=r.POST or None)
    if r.method=="POST":
        if form.is_valid():
            user=form.get_user()
            login_user(r,user)
            return redirect("home")
    return render(r,"registration/login.html",{"form":form})

def logout(r):
    logout_user(r)
    return redirect("home")



        
    





