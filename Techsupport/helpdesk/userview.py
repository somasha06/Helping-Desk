from django.shortcuts import render,redirect,get_object_or_404
from helpdesk.models import Supportticket,Ticketattachment,Ticketcomment
from .userform import SupportTicketForm,TicketAttachmentForm,TicketCommentForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required()
@role_required(allowed_roles={"user"})
def userdashboard(request):
    countticket={
        'openticket':Supportticket.objects.filter(status='open', created_by=request.user).count(),
        'closedticket':Supportticket.objects.filter(status='closed',created_by=request.user).count(),
        'inprogressticket':Supportticket.objects.filter(status='inprogress',created_by=request.user).count(),
    }
    return render(request,'user/userdashboard.html',countticket)

@login_required()
@role_required(allowed_roles={"user"})
def userhome(request):
     return render(request,"user/userhome.html")

@login_required()
@role_required(allowed_roles={"user"})
def usertickets(request):
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

        return redirect('usertickets')  
    
    myticket=Supportticket.objects.filter(created_by=request.user)

    return render(request,'user/usertickets.html',{"myticket":myticket})

@login_required()
@role_required(allowed_roles={"user"})
def iscomplete(r,id):
    ticket=SupportTicketForm.objects.get(id=id)
    ticket.is_completed=True
    ticket.status='closed'
    ticket.save()
    return redirect('usertickets')

@login_required()
@role_required(allowed_roles={"user"})
def userticketdetail(request,id):
   
        ticket=Supportticket.objects.get(id=id,created_by=request.user)
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
                  return redirect("userticketdetail",id=id)


        return render(request,'user/userticketdetail.html',context)