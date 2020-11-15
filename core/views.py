from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import FlightTicket, Flight_Booking_List, Transactions
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

def ticket_list(request):           #used instead of item_list
    context={
        'tickets': FlightTicket.objects.all()
    }
    return render(request, "ticket_list.html", context)


def home_v(request):
    return render(request, "index.html")

def destination(request):
    return render(request, "destination.html")

def pricing(request):
    return render(request, "pricing.html")

def contact(request):
    return render(request, "contact.html")

def flights(request):
    context = {
        'object_list': FlightTicket.objects.all()
    }
    return render(request, "flights_results.html", context)

def seats(request):
    return render(request, "seats.html")