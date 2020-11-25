from django.conf import settings 
from django.db import models
from django.shortcuts import reverse

# Create your models here.

class FlightTicket(models.Model):
    airline = models.CharField(max_length = 100,blank=True, null=True)
    flight_no = models.CharField(max_length = 10,blank=True, null=True)
    start = models.CharField(max_length = 100, blank=True, null=True)
    start_code = models.CharField(max_length=10, blank=True, null=True)
    destination = models.CharField(max_length = 100, blank=True, null=True)
    destination_code = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    duration_hr = models.IntegerField(default=0)
    duration_min = models.IntegerField(default=0)
    number_seats = models.IntegerField(default=26)
    # economy seats
    number_seats_available = models.IntegerField(default=20)
    # first class seats
    first_class_seats = models.IntegerField(default=6)
    price = models.FloatField()
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="airlines", blank=True)


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

    def first_class_price(self):
        price = self.price*1.10
        return price


class Flight_Booking_List(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ticket = models.ForeignKey(FlightTicket, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    last_booked = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, null=True)
    seats_class = models.CharField(max_length=100, blank=True, null=True)
    additional = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.ticket.flight_no

    def additional_charge(self):
        return self.additional

    def final_amount(self):
        if self.seats_class == 'first':
            amount = (self.ticket.price * self.quantity)*1.10
        else:
            amount = (self.ticket.price * self.quantity)
        return amount

    def tax_percent(self):
        if self.seats_class == 'first':
            tax = 12
        else:
            tax = 5
        return tax

    def tax(self):
        amount = self.final_amount()
        if self.seats_class == 'first':
            tax = 0.12*amount
        else:
            tax = 0.05*amount
        return tax

    def amount_after_tax(self):
        amount = self.final_amount()
        if self.seats_class == 'first':
            amount += 0.12*amount
        else:
            amount += 0.05*amount
        return amount

    def update_no_seats(self):
        self.ticket.number_seats_available = self.ticket.number_seats_available - self.quantity
        self.ticket.save()

    def update_no_seats_fc(self):
        self.ticket.first_class_seats = self.ticket.first_class_seats - self.quantity
        self.ticket.save()

    def class_display(self):
        if self.seats_class == 'first':
            return 'First Class'
        else:
            return 'Economy'

class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 100,blank=True, null=True)
    last_name = models.CharField(max_length = 100,blank=True, null=True)
    tickets = models.ManyToManyField(Flight_Booking_List)          #used instead of items
    booked_date = models.DateTimeField()                    #used instead of ordered_date
    booked = models.BooleanField(default=False)             #used instead of ordered
    seats_class = models.CharField(max_length = 100,blank=True, null=True)
    discount_val = models.IntegerField(blank=True, null=True)

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
                ticket.last_booked = True
                ticket.save()

    def class_update(self):
        for ticket in self.tickets.all():
            seats_class = self.seats_class
            if ticket.booked is False:
                if seats_class == 'economy':
                    ticket.seats_class = 'economy'
                else:
                    ticket.seats_class = 'first'
                ticket.save()

    def update_additional(self, value, num):
        for ticket in self.tickets.all():
            if ticket.booked is False:
                ticket.additional += value*num
                ticket.save()

    def total_amount(self):
        total = 0
        for order_item in self.tickets.all():
            total += order_item.final_amount()
        return total

    def total_additional(self):
        total = 0
        for order_item in self.tickets.all():
            total += order_item.additional
        return total

    def tax(self):
        total = 0
        for order_item in self.tickets.all():
            total += order_item.tax()

        return total

    def total_amount_tax(self):
        total = 0
        for order_item in self.tickets.all():
            total += order_item.amount_after_tax()
        total += self.total_additional()
        return total

    def update_discount(self, value):
        self.discount_val = value
        self.save()


    def discount(self):
        discount_val = 1 - self.discount_val/100
        total = 0
        for order_item in self.tickets.all():
            total += order_item.amount_after_tax()
        total += self.total_additional()
        total = total * discount_val
        return total


    def update_seats(self):
        for ticket in self.tickets.all():
            if ticket.booked is False:
                ticket.update_no_seats()
                ticket.save()

    def update_seats_fc(self):
        for ticket in self.tickets.all():
            if ticket.booked is False:
                ticket.update_no_seats_fc()
                ticket.save()


class Destination(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="destination", blank=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    quote = models.CharField(max_length=500,blank=True, null=True)
    things_to_do = models.CharField(max_length=500,blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    map = models.ImageField(upload_to="destination", blank=True)

    def __str__(self):
        return self.name

    def get_abs_url(self):
        return reverse("core:destination_details", kwargs={
            'slug': self.slug
        })

