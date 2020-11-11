from django.conf import settings 
from django.db import models

# Create your models here.

class FlightTicket(models.Model):                           #used instead of Item 
    title = models.CharField(max_length = 100)
    price = models.FloatField()                             

    def __str__(self):
        return self.title

class FlightBooked(models.Model):                           #used instead of OrderItem
    ticket = models.ForeignKey(FlightTicket, on_delete=models.CASCADE)  #used instead of item 

    def __str__(self):
        return self.title

class Transactions(models.Model):                           #used instead of Order  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    tickets = models.ManyToManyField(FlightBooked)          #used instead of items 
    booked_date = models.DateTimeField()                    #used instead of ordered_date
    booked = models.BooleanField(default=False)             #used instead of ordered 

    def __str__(self):
        return self.user.username
