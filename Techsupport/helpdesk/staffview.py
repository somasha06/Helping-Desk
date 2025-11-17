from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Supportticket, Ticketcomment,Userrole,Ticketattachment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm

def staffdashboard(request):
    return render(request,"staff/staffdashboard.html")

def staffhome(request):
    return render(request,"staff/staffhome.html")