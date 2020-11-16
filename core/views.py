from django.shortcuts import render, get_object_or_404, redirect
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
    if request.method == 'GET':
        from_place = request.GET.get('from-place')
        to_place = request.GET.get('to-place')
        start_date = request.GET.get('start_date')
        adults = request.GET.get('adults')
        children = request.GET.get('children')
        seats_required = int(adults) + int(children)
        if from_place is not None and to_place is not None and start_date is not None and seats_required is not None:
            lookups = Q(start__icontains=from_place, destination__icontains=to_place, date=start_date, number_seats_available__gte = seats_required   )

            results = FlightTicket.objects.filter(lookups)

            context = {'object_list': results}

            return render(request, 'flights_results.html', context)

        else:
            return render(request, 'flights_results.html')

    else:
        return render(request, 'flights_results.html')


def seats(request):
    return render(request, "seats.html")

class flight_details_V(DetailView):
    model = FlightTicket
    template_name = "flight_details.html"