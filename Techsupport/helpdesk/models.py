from django.db import models
from django.contrib.auth.models import User

class Userrole(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_name")
    role=models.CharField(max_length=200,choices=(("user","user"),("staff","staff"),("admin","admin")))

    def __str__(self):
        return self.user
    
class Supportticket(models.Model):
    title=models.CharField(max_length=200)
    status=models.CharField(max_length=200,choices=(("open","open"),("in_progress","in_progress"),("closed","closed")))
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    description=models.TextField()
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="assigned_to",null=True,blank=True)

    def __str__(self):
        return self.title
    
class Ticketcomment(models.Model):
    ticket=models.ForeignKey(Supportticket,on_delete=models.CASCADE,related_name="comments")
    commented_by=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)


class Ticketattachment(models.Model):
    ticket=models.ForeignKey(Supportticket,on_delete=models.CASCADE,related_name="attachments")
    file=models.FileField(upload_to='ticket_attachments/')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE)
   