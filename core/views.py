from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import FlightTicket, Flight_Booking_List, Transactions
from .forms import conformation_form, payment_form
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
        seat_class = request.GET.get('class')
        seats_required = int(adults) + int(children)
        if seats_required != 0:

            if from_place is not None and to_place is not None and start_date is not None:
                if seat_class == 'first':
                    lookups = Q(start__icontains=from_place, destination__icontains=to_place, date=start_date, first_class_seats__gte = seats_required   )

                else:
                    lookups = Q(start__icontains=from_place, destination__icontains=to_place, date=start_date,
                                number_seats_available__gte=seats_required)

                results = FlightTicket.objects.filter(lookups)

                context = {'object_list': results,
                           'seats_required':seats_required}

                return render(request, 'flights_results.html', context)

            else:
                return render(request, 'flights_results.html')
        else:
            # messages.error(request, "Please enter the number of adults/children")
            return render(request, 'index.html')


    else:
        return render(request, 'flights_results.html')


def seats(request):
    return render(request, "seats.html")

def my_account(request):
    user = request.user.username
    content={
        'user' : user
    }
    return render(request, "my_account.html", content)

def my_flights(request):
    user = request.user.username
    my_flight_list = Flight_Booking_List.objects.filter(user=request.user, booked=True)
    content = {
        'user': user,
        'flights': my_flight_list
    }
    return render(request, "my_flights.html", content)

def flight_details_V(request, slug):
    flight = get_object_or_404(FlightTicket, slug=slug)
    price = flight.first_class_price()
    content = {
        'object': flight,
        'first_class_price' :price
    }
    return render(request, 'flight_details.html', content)


@login_required
def add_to_cart(request, slug):
        flight = get_object_or_404(FlightTicket, slug=slug)
        orderItem, created = Flight_Booking_List.objects.get_or_create(
            ticket=flight,
            user=request.user,
            booked=False
        )
        order_date = timezone.now()
        order = Transactions.objects.create(user=request.user, booked_date=order_date)
        order.tickets.add(orderItem)
        #messages.success(request, "Almost done!")
        return redirect("core:confirmation")


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class confirmation(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        form = conformation_form()
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)
            context = {
                'object': order,
                'form': form
            }

            return render(self.request, "details_confirmation.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = conformation_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                number_of_seats = form.cleaned_data.get('number_of_seats')
                seats_class = form.cleaned_data.get('seats_class')

                if is_valid_form([first_name, last_name, number_of_seats]):
                    order.first_name = first_name
                    order.last_name = last_name
                    order.flight_seats(number_of_seats)
                    order.seats_class = seats_class
                    order.save()


                else:
                    messages.info(self.request, "Please fill in the required fields")

                #messages.success(self.request, "Almost Done")
                return redirect('core:payment')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")

class payment_View(View):
    def get(self, *args, **kwargs):
        form = payment_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)
            context = {
                'object': order,
                'form' : form
            }
            return render(self.request, "payment.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = payment_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                card_no = form.cleaned_data.get('Card_Number')
                otp = form.cleaned_data.get('OTP')

                if is_valid_form([card_no, otp]):
                    if order.seats_class == 'economy':
                        order.update_seats()
                    else:
                        order.update_seats_fc()
                    order.flight_booked()
                    order.booked = True
                    order.save()

                else:
                    messages.info(self.request, "Please fill in the required fields")

                messages.success(self.request, "Congratulations!! You have successfully booked your flight!")
                return redirect('core:home')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")