from django.contrib import admin
from .models import FlightTicket, Flight_Booking_List, Transactions

admin.site.register(FlightTicket)
admin.site.register(Flight_Booking_List)
admin.site.register(Transactions)