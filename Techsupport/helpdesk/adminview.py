from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole,Ticketattachment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm


def admindashboard(request):   

    count={
        "users":User.objects.count(),
        "tickets":Supportticket.objects.count(),
        "reply":Ticketcomment.objects.count(),
        "staff":Userrole.objects.filter(role="staff").count(),
        "resolved_tickets":Supportticket.objects.filter(status="closed").count(),        
    }

    return render(request,"admin/admindashboard.html",count)

def adminhome(request):
    return render(request,"admin/adminhome.html")

def manageusers(r):

    data={
        "users" : Userrole.objects.filter(role="user"),
    }
    return render(r,"admin/manageuser.html",data)

def reports(r):
    return render(r, 'admin/report.html')

def adminsettings(r):
    return render(r, 'admin/setting.html')

def managestaff(request):

    staff_users = User.objects.filter(roleinfo__role="staff")   

    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")

        staff = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        staff.is_staff = True     
        staff.save()

        Userrole.objects.create(account=staff,role="staff")

        return redirect("createstaff")

    return render(request, 'admin/managestaff.html',{"staff_users": staff_users})

def managetickets(request):
    if request.method == "POST":
        title=request.POST.get('title')
        description=request.POST.get('description')

        newticket=Supportticket.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            status="open"
        )

        if "attachments" in request.FILES:
            attachments=request.FILES.getlist('attachments')
            for file in attachments:
                Ticketattachment.objects.create(file=file,ticket=newticket,uploaded_by=request.user)

        return redirect('managetickets')  
    
    myticket=Supportticket.objects.all()

    return render(request,'admin/manageticket.html',{"myticket":myticket})


def adminview(request,id):
   
        ticket=Supportticket.objects.get(id=id)
        attachments = Ticketattachment.objects.filter(ticket=ticket)
        comments=Ticketcomment.objects.filter(ticket=ticket)
        
        form=TicketCommentForm(request.POST or None, request.FILES or None)
                     
        context={
            'ticket':ticket,
            'attachments':attachments,
            'comments':comments,
            'form':form
        }

        if request.method == "POST":
             if form.is_valid():
                  reply=form.save(commit=False)
                  reply.ticket=ticket
                  reply.commented_by=request.user
                  reply.save()

                  ticket.assigned_to=request.user
                  ticket.status="in_progress"
                  ticket.save()
                  return redirect("adminview",id=id)

                  

        return render(request,'admin/adminview.html',context)

def createstaff(request):

    staff_users = User.objects.filter(roleinfo__role="staff")   

    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")

        staff = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Userrole.objects.create(account=staff,role="staff")

        return redirect("createstaff")
    return render(request,"admin/createstaff.html",{"staff_users": staff_users})

def removestaff(request,id):
    remove=User.objects.get(id=id)
    remove.delete()
    return redirect(managestaff)


# def editstaffdetail(request,id):

#     staff=User.objects.get(id=id)

#     if request.method == "POST":
#         staff.username=request.POST.get("username")
#         staff.email=request.POST.get("email")

#         password=request.POST.get("password")
#         if password:
#             staff.set_password(password)

#             staff.save()

#             roleinfo = Userrole.objects.get(account=staff)
#             roleinfo.account = staff
#             roleinfo.save()

#             return redirect(managestaff)
        
#     return render(request,"admin/editstaffdetail.html",{"staff":staff})

def staffticketdetails(request, id):
    # Get the staff user by ID
    staff = User.objects.get(id=id)

    # Filter tickets assigned to this staff
    opentickets = Supportticket.objects.filter(status="open")
    inprogresstickets = Supportticket.objects.filter(status="in_progress", assigned_to=staff)
    closedtickets = Supportticket.objects.filter(status="closed", assigned_to=staff)

    data = {
        "staff": staff,
        "opentickets": opentickets,
        "inprogresstickets": inprogresstickets,
        "closedtickets": closedtickets,
    }

    return render(request, "admin/viewstaffdetail.html", data)

def assignticket(request,id,staff_id):
    
    ticket=Supportticket.objects.get(id=id)
    staff=User.objects.get(id=staff_id)

    if ticket.assigned_to is None:
        ticket.assigned_to = staff
        ticket.status="in_progress"
        ticket.save()

    return redirect(staffticketdetails,staff_id)


