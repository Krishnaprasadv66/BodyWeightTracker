from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class weightlist(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight =  models.FloatField()
    timeOfmarking= models.TimeField(auto_now=True)
    dateOfMarking = models.DateField(auto_now_add =True) 