from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole,Ticketattachment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required


@login_required()
@role_required(allowed_roles={"admin"})
def admindashboard(request):   

    count={
        "users":User.objects.count(),
        "tickets":Supportticket.objects.count(),
        "reply":Ticketcomment.objects.count(),
        "staff":Userrole.objects.filter(role="staff").count(),
        "customer":Userrole.objects.filter(role="user").count(),
        "resolved_tickets":Supportticket.objects.filter(status="closed").count(),        
        "inprogress_tickets":Supportticket.objects.filter(status="in_progress").count(),        
        "open_tickets":Supportticket.objects.filter(status="open").count(),  
        # "opentickets":Supportticket.objects.filter(status="open",created_by="user").count()      
    }

    return render(request,"admin/admindashboard.html",count)

@login_required()
@role_required(allowed_roles={"admin"})
def adminhome(request):
    return render(request,"admin/adminhome.html")

@login_required()
@role_required(allowed_roles={"admin"})
def manageusers(request):
    customer_users = User.objects.filter(roleinfo__role="user") 
    for customer in customer_users:
        customer.open_tickets = Supportticket.objects.filter(created_by=customer, status='open').count()
        customer.inprogress_tickets = Supportticket.objects.filter(created_by=customer, status='in_progress').count()
        customer.closed_tickets = Supportticket.objects.filter(created_by=customer, status='closed').count()
        customer.total_tickets = Supportticket.objects.filter(created_by=customer).count()
        
    return render(request,"admin/manageuser.html",{"customer_users":customer_users})

@login_required()
@role_required(allowed_roles={"admin"})
def reports(r):
    return render(r, 'admin/report.html')

@login_required()
@role_required(allowed_roles={"admin"})
def adminsettings(r):
    return render(r, 'admin/setting.html')

@login_required()
@role_required(allowed_roles={"admin"})
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

def viewuserdetails(request,id):
    customer_user=User.objects.get(id=id) 
    opentickets = Supportticket.objects.filter(status="open",created_by=customer_user)
    inprogresstickets = Supportticket.objects.filter(status="in_progress", created_by=customer_user)
    closedtickets = Supportticket.objects.filter(status="closed", created_by=customer_user)

    data = {
        "customer_user": customer_user,
        "opentickets": opentickets,
        "inprogresstickets": inprogresstickets,
        "closedtickets": closedtickets,
    }

    return render(request, "admin/viewuserdetail.html",data)

@login_required()
@role_required(allowed_roles={"admin"})
def managetickets(request):
    if request.method == "POST":
        title=request.POST.get('title')
        description=request.POST.get('description')

        newticket=Supportticket.objects.create(
            title=title,
            description=description,
            created_by=request.user,  #*here admin will create ticket for customer how he will do that ??/??????????????????
            status="open"
        )

        if "attachments" in request.FILES:
            attachments=request.FILES.getlist('attachments')
            for file in attachments:
                Ticketattachment.objects.create(file=file,ticket=newticket,uploaded_by=request.user)

        return redirect('managetickets')  
    
    myticket=Supportticket.objects.all()

    return render(request,'admin/manageticket.html',{"myticket":myticket})

@login_required()
@role_required(allowed_roles={"admin"})
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

@login_required()
@role_required(allowed_roles={"admin"})
def createstaff(request):

    staff_users = User.objects.filter(roleinfo__role="staff")   #From User i.e account, go to Userrole, then access its role field ("__" means Traverse relationship or go inside)

    if request.method == "POST":
        username=request.POST.get("username") #the first username is variable and the second username is the name =username coming from template
        email=request.POST.get("email")
        password=request.POST.get("password")

        staff = User.objects.create_user(  #create_user() is provided by Django’s User Manager.It comes with Django automatically when you use: from django.contrib.auth.models import User it hashes the password ,handle usename email properly but create doesn't hashes password
            username=username, #here first username is model field and second username is variable where we stored the data via form above 
            email=email,
            password=password
        )   

        Userrole.objects.create(account=staff,role="staff") # account is the model field where we are storing staff that i created above and role(model field)=staff(string and in defined in field) is just telling about it's role 

        return redirect("createstaff")
    return render(request,"admin/createstaff.html",{"staff_users": staff_users})

@login_required()
@role_required(allowed_roles={"admin"})
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

@login_required()
@role_required(allowed_roles={"admin"})
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

def closeticket(request,id):
    ticket=Supportticket.objects.get(id=id)   
    ticket.status = "closed"
    ticket.save()
 
    return redirect(managetickets) 

@login_required()
@role_required(allowed_roles={"admin"})
def assignticket(request,id,staff_id):
    
    ticket=Supportticket.objects.get(id=id)
    staff=User.objects.get(id=staff_id)

    if ticket.assigned_to is None:
        ticket.assigned_to = staff
        ticket.status="in_progress"

        ticket.save()

    return redirect(staffticketdetails,staff_id)


@login_required()
@role_required(allowed_roles={"admin"})
def viewfulluserdetail(request,id):
   
        ticket = get_object_or_404(Supportticket, id=id)
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
                  return redirect("viewuserdetail",id=id)


        return render(request,'admin/viewfulluserdetail.html',context)


def admin_reports(request):
    admin=request.user
    total_tickets=Supportticket.objects.count()
    open_ticket=Supportticket.objects.filter(status="open").count()
    in_progressticket=Supportticket.objects.filter(status="in_progress").count()
    closed_ticket=Supportticket.objects.filter(status="closed").count()

    if total_tickets>0:
        openpercent=round((open_ticket/total_tickets)*100,2)
        in_progresspercent=round((in_progressticket/total_tickets)*100,2)
        closedpercent=round((closed_ticket/total_tickets)*100,2)

    else:
        openpercent = in_progresspercent = closedpercent = 0

    if openpercent>closedpercent and in_progresspercent>closedpercent :
        performance="Bad"
    
    elif closedpercent>70:
        performance="Good"
    else:
        performance="Average"

    context = {
        'total_tickets': total_tickets,
        'open_ticket': open_ticket,
        'in_progressticket': in_progressticket,
        'closed_ticket': closed_ticket,
        'openpercent': openpercent,
        'in_progresspercent': in_progresspercent,
        'closedpercent': closedpercent,
        'performance':performance,
    }

    return render(request, 'admin/admin_reports.html', context)