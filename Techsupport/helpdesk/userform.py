from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # role=forms.ChoiceField(choices=Userrole.role)
    email=forms.EmailField(required=True)
    
    class Meta:
        model= User
        fields = ['username','email','password1','password2']

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

