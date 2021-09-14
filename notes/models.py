# from notes.views import contact
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.

class Signup(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    contact=models.CharField(max_length=10,null=True)
    branch=models.CharField(max_length=30,null=True)
    role=models.CharField(max_length=15,null=True)

    # def __str__(self):
    #     return self.user.username


class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    uploadingdate=models.CharField(max_length=30,null=True)
    branch=models.CharField(max_length=30)
    subject=models.CharField(max_length=30)
    notesfile=models.FileField(null=True)
    filetype=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=15)

    def __str__(self):
        return self.user.username+" "+self.status

    
