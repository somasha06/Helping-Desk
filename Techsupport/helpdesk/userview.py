from django.shortcuts import render,redirect
from helpdesk.models import Supportticket
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm

def userdashboard(r):
    # countticket={
    #     'openticket':Supportticket.objects.filter(status='open', created_by=r.user).count(),
    #     'closedticket':Supportticket.objects.filter(status='closed',created_by=r.user).count(),
    #     'inprogressticket':Supportticket.objects.filter(status='inprogress',created_by=r.user).count(),
    # }
    return render(r,'user/userdashboard.html')

def usertickets(r):
    ticketform=SupportTicketForm(r.POST or None, r.FILES or None)
    attachmentform=TicketAttachmentForm(r.POST or None, r.FILES or None)
    commentsform=TicketCommentForm(r.POST or None, r.FILES or None)

    tickets=Supportticket.objects.filter(created_by=r.user)
    if r.method == "POST":
        if ticketform.is_valid() and attachmentform.is_valid() and commentsform.is_valid():

            ticket=ticketform.save(commit=False)
            ticket.created_by=r.user
            ticket.status='open'
            ticket.save()

            attachment=attachmentform.save(commit=False)
            attachment.ticket=ticket
            attachment.uploaded_by=r.user
            attachment.save()

            comment=commentsform.save(commit=False)
            comment.ticket=ticket
            comment.commented_by=r.user
            comment.save()
            return redirect('usertickets')  
    return render(r,'user/usertickets.html',{'ticketform':ticketform,'attachmentform':attachmentform,'commentsform':commentsform,'tickets':tickets})

def iscomplete(r,id):
    ticket=SupportTicketForm.objects.get(id=id)
    ticket.is_completed=True
    ticket.status='closed'
    ticket.save()
    return redirect('usertickets')

def userticketdetail(r,id):
    details=Supportticket.objects.get(id=id)
    replies=details.comments.all()

    if r.method == "POST":
        commentform=TicketCommentForm(r.POST or None, r.FILES or None)
        attachmentform=TicketAttachmentForm(r.POST or None, r.FILES or None)

        if commentform.is_valid() and attachmentform.is_valid():
            comment=commentform.save(commit=False)
            comment.ticket=details
            comment.commented_by=r.user
            comment.save()

            attachment=attachmentform.save(commit=False)
            attachment.ticket=details
            attachment.uploaded_by=r.user
            attachment.save()

            return redirect('userticketdetail', id=id)
        
    return render(r,'user/userticketdetail.html',{'details':details,'replies':replies,'commentform':TicketCommentForm(),'attachmentform':TicketAttachmentForm()})