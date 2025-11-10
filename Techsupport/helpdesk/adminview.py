from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole
from .adminform import ASupportTicketForm, ATicketAttachmentForm, ATicketCommentForm


def admindashboard(r):
    count={
        "users":User.objects.count(),
        "tickets":Supportticket.objects.count(),
        "reply":Ticketcomment.objects.count(),
        "agents":Userrole.objects.filter(role="staff").count(),
        "resolved_tickets":Supportticket.objects.filter(status="closed").count(),
    }
    return render(r,"admin/admindashboard.html",{"count":count})

def manageusers(r):
   

    data={
        "users" : User.objects.filter(is_superuser=False),
    }
    return render(r,"admin/manageusers.html",data)

def managetickets(r):
        data = {
        "tickets" : Supportticket.objects.all()
    }
        return render(r,"admin/manageticket.html",data)

def viewticket(r):
    return render(r,"admin/viewticket.html")

def reports(r):
    return render(r, 'admin/report.html')

def adminsettings(r):
    return render(r, 'admin/setting.html')

def manageagents(r):
    return render(r, 'admin/manageagents.html')

def usertickets(r):
    Aticketform=ASupportTicketForm(r.POST or None, r.FILES or None)
    Aattachmentform=ATicketAttachmentForm(r.POST or None, r.FILES or None)
    Acommentsform=ATicketCommentForm(r.POST or None, r.FILES or None)

    tickets=Supportticket.objects.filter(created_by=r.user)
    if r.method == "POST":
        if Aticketform.is_valid() and Aattachmentform.is_valid() and Acommentsform.is_valid():

            ticket=Aticketform.save(commit=False)
            ticket.created_by=r.user
            ticket.status='open'
            ticket.save()

            attachment=Aattachmentform.save(commit=False)
            attachment.ticket=ticket
            attachment.uploaded_by=r.user
            attachment.save()

            comment=Acommentsform.save(commit=False)
            comment.ticket=ticket
            comment.commented_by=r.user
            comment.save()
            return redirect('managetickets')  
    return render(r,'admin/manageticket.html',{'Aticketform':Aticketform,'Aattachmentform':Aattachmentform,'Acommentsform':Acommentsform,'tickets':tickets})