from django.conf import settings 
from django.db import models
from django.shortcuts import reverse

# Create your models here.

class FlightTicket(models.Model):
    airline = models.CharField(max_length = 100,blank=True, null=True)
    flight_no = models.CharField(max_length = 10,blank=True, null=True)
    start = models.CharField(max_length = 100, blank=True, null=True)
    destination = models.CharField(max_length = 100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    arrival_time =  models.TimeField(blank=True, null=True)
    number_seats = models.IntegerField(default=26)
    number_seats_available = models.IntegerField(default=26)
    price = models.FloatField()
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.flight_no

    def get_abs_url(self):
        return reverse("core:flight_details", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

class Flight_Booking_List(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ticket = models.ForeignKey(FlightTicket, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.ticket.flight_no

class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 100,blank=True, null=True)
    last_name = models.CharField(max_length = 100,blank=True, null=True)
    tickets = models.ManyToManyField(Flight_Booking_List)          #used instead of items
    booked_date = models.DateTimeField()                    #used instead of ordered_date
    booked = models.BooleanField(default=False)             #used instead of ordered 

    def __str__(self):
        return self.user.username

    def flight_seats(self, seats):
        for ticket in self.tickets.all():
            if ticket.booked is False:
                ticket.quantity = seats
                ticket.save()

    def flight_booked(self):
        for ticket in self.tickets.all():
            if ticket.booked is False:
                ticket.booked = True
                ticket.save()
