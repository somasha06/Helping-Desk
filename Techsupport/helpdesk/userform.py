from django.forms import ModelForm
from .models import Supportticket, Ticketattachment,Ticketcomment

class SupportTicketForm(ModelForm):
    class Meta:
        model = Supportticket
        fields = ['title']

class TicketAttachmentForm(ModelForm):
    class Meta:
        model = Ticketattachment
        fields = ['file']

class TicketCommentForm(ModelForm):
    class Meta:
        model = Ticketcomment
        fields = ['comment']