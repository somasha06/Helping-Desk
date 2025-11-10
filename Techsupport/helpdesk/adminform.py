from django.forms import ModelForm
from .models import Supportticket, Ticketattachment,Ticketcomment

class ASupportTicketForm(ModelForm):
    class Meta:
        model = Supportticket
        fields = ['title','description','created_by','status']

class ATicketAttachmentForm(ModelForm):
    class Meta:
        model = Ticketattachment
        fields = ['file']

class ATicketCommentForm(ModelForm):
    class Meta:
        model = Ticketcomment
        fields = ['comment','commented_by']