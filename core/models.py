from django.conf import settings 
from django.db import models

# Create your models here.

class FlightTicket(models.Model):
    airline = models.CharField(max_length = 100,blank=True, null=True)
    flight_no = models.CharField(max_length = 10,blank=True, null=True)
    start = models.CharField(max_length = 100, blank=True, null=True)
    destination = models.CharField(max_length = 100, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    number_seats = models.IntegerField(default=26)
    number_seats_available = models.IntegerField(default=26)
    price = models.FloatField()

    def __str__(self):
        return self.flight_no

class Flight_Booking_List(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ticket = models.ForeignKey(FlightTicket, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.ticket.flight_no

class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    tickets = models.ManyToManyField(Flight_Booking_List)          #used instead of items
    booked_date = models.DateTimeField()                    #used instead of ordered_date
    booked = models.BooleanField(default=False)             #used instead of ordered 

    def __str__(self):
        return self.user.username
