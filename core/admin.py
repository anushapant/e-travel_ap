from django.contrib import admin
from .models import FlightTicket, FlightBooked, Transactions 

admin.site.register(FlightTicket)
admin.site.register(FlightBooked)
admin.site.register(Transactions)