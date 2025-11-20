from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole,Ticketattachment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm

def staffdashboard(request):
    return render(request,"staff/staffdashboard.html")

def staffhome(request):
    return render(request,"staff/staffhome.html")

def staffmanagetickets(request):    
    unassigned=Supportticket.objects.filter(assigned_to=None)
    myassigned=Supportticket.objects.filter(assigned_to=request.user)

    myticket = unassigned | myassigned
    return render(request,'staff/staffmanageticket.html',{"myticket":myticket})


def staffviewdetail(request,id):
   
        ticket=Supportticket.objects.get(id=id)
        # if ticket.assigned_to != request.user:
        #     return redirect("staffmanagetickets")

        # if ticket.status == "closed":
        #     return redirect("staffmanagetickets")

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

def taketicket(request,id):
    ticket=Supportticket.objects.get(id=id)
    if ticket.assigned_to is None:
        ticket.assigned_to=request.user
        ticket.status="in_progress"
        ticket.save()

    return redirect(staffmanagetickets)

def closeticket(request,id):
    ticket=Supportticket.objects.get(id=id)

    if ticket.assigned_to == request.user:
        ticket.status == "closed"
        ticket.save()
 
    return redirect(staffmanagetickets) 