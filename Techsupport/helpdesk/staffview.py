from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole,Ticketattachment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required()
@role_required(allowed_roles={"staff"})
def staffdashboard(request):
    count={
        "opentickets":Supportticket.objects.filter(status='open',assigned_to=request.user).count(),
        "closedtickets":Supportticket.objects.filter(status='closed',assigned_to=request.user).count(),
        "staff":Userrole.objects.filter(role="staff").count(),
        "inprogresstickets":Supportticket.objects.filter(status="in_progress",assigned_to=request.user).count(),        
    }
    return render(request,"staff/staffdashboard.html",count)

@login_required()
@role_required(allowed_roles={"staff"})
def staffhome(request):
    return render(request,"staff/staffhome.html")

@login_required()
@role_required(allowed_roles={"staff"})
def staffmanagetickets(request):    
    
    opentickets = Supportticket.objects.filter(status="open")
    inprogresstickets=Supportticket.objects.filter(status="in_progress",assigned_to=request.user)
    closedtickets=Supportticket.objects.filter(status="closed",assigned_to=request.user)

    data = {
        "opentickets": opentickets,
        "inprogresstickets": inprogresstickets,
        "closedtickets": closedtickets,
    }

    return render(request,'staff/staffmanageticket.html',data)

@login_required()
@role_required(allowed_roles={"staff"})
def staffviewdetail(request,id):
   
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
                  return redirect("staffviewdetail",id=id)

        return render(request,'staff/staffviewdetail.html',context)

@login_required()
@role_required(allowed_roles={"staff"})
def taketicket(request,id):
    ticket=Supportticket.objects.get(id=id)
    if ticket.assigned_to is None:
        ticket.assigned_to=request.user
        ticket.status="in_progress"
        ticket.save()

    return redirect(staffmanagetickets)

@login_required()
# @role_required(allowed_roles={"staff"})
def closeticket(request,id):
    ticket=Supportticket.objects.get(id=id)   
    ticket.status = "closed"
    ticket.save()
 
    return redirect(staffmanagetickets) 

def staff_user(request):
    staff=request.user
    users=User.objects.filter(supportticket__assigned_to=staff).distinct()
    return render(request,"staff/staff_user.html",{'users':users})

def staff_reports(request):
    staff=request.user
    total_tickets=Supportticket.objects.filter(assigned_to=staff).count()
    open_ticket=Supportticket.objects.filter(assigned_to=staff,status="open").count()
    in_progressticket=Supportticket.objects.filter(assigned_to=staff,status="in_progress").count()
    closed_ticket=Supportticket.objects.filter(assigned_to=staff,status="closed").count()

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
        'performance':performance
    }

    return render(request, 'staff/staff_reports.html', context)