from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import FlightTicket, Flight_Booking_List, Transactions, Destination
from .forms import confirmation_form, payment_form, confirmation_form2, round_tripF, discount_form
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Home page
def home_v(request):
    return render(request, "index.html")

# Destinations page
def destination(request):
    object_list = Destination.objects.all()
    content = {
        'object_list':object_list
    }
    return render(request, "destination.html", content)

# Contact Us page
def contact(request):
    return render(request, "contact.html")

# Contact Us page
def special_assistance(request):
    return render(request, "special_assistance.html")

# Flights search result page
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

def seats_new(request):
    return render(request, "seats_new.html")

# My account page
def my_account(request):
    user = request.user.username
    content={
        'user' : user
    }
    return render(request, "my_account.html", content)

# My flights page (list of flights the user has booked)
def my_flights(request):
    user = request.user.username
    my_flight_list = Flight_Booking_List.objects.filter(user=request.user, booked=True)
    content = {
        'user': user,
        'flights': my_flight_list
    }
    return render(request, "my_flights.html", content)

# Page for Flight details
def flight_details_V(request, slug):
    flight = get_object_or_404(FlightTicket, slug=slug)
    price = flight.first_class_price()
    content = {
        'object': flight,
        'first_class_price' :price
    }
    return render(request, 'flight_details.html', content)

# Destination details page
def destination_details_V(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    content = {
        'object': destination
    }
    return render(request, 'destination_details.html', content)

# Booking confirmed page, final step
def booking_confirmed(request):
    return render(request, "booking_confirmed.html")

# adding flights to the 'cart'
@login_required
def add_to_cart(request, slug):
    flight = get_object_or_404(FlightTicket, slug=slug)
    orderItem, created = Flight_Booking_List.objects.get_or_create(
            ticket=flight,
            user=request.user,
            booked=False
    )

    q = Transactions.objects.filter(user=request.user, booked=False)

    if q.exists():
        ticket = q[0]
        ticket.tickets.add(orderItem)

        return redirect("core:confirmation2")

    else:
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

# Details confirmation
class confirmation(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        form = confirmation_form()
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
        form = confirmation_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                number_of_seats = form.cleaned_data.get('number_of_seats')
                seats_class = form.cleaned_data.get('seats_class')
                round_trip = form.cleaned_data.get('round_trip')
                meal = form.cleaned_data.get('meals')
                wheelchair = form.cleaned_data.get('wheelchair')
                stroller = form.cleaned_data.get('stroller')
                services = form.cleaned_data.get('services')
                lounge = form.cleaned_data.get('lounge')

                if is_valid_form([first_name, last_name, number_of_seats, round_trip, meal]):
                    order.first_name = first_name
                    order.last_name = last_name
                    order.flight_seats(number_of_seats)
                    order.seats_class = seats_class
                    if order.seats_class == 'economy':
                        order.update_seats()
                    else:
                        order.update_seats_fc()

                    if meal == 'veg':
                        order.update_additional(10, number_of_seats)
                    elif meal == 'non-veg':
                        order.update_additional(12, number_of_seats)
                    else:
                        None

                    if services == 'um':
                        order.update_additional(25, 1)

                    if lounge == 'yes':
                        if seats_class == 'economy':
                            order.update_additional(10, number_of_seats)
                        else:
                            #No additional charge if your ticket is a first class one
                            None

                    order.flight_booked()
                    order.save()

                else:
                    messages.info(self.request, "Please fill in the required fields")

                if round_trip == 'no':
                    #messages.success(self.request, "Almost Done")
                    return redirect('core:discount')

                else:
                    return redirect('core:round_trip')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")


# Details confirmation 2
class confirmation2(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        form = confirmation_form2()
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
        form = confirmation_form2(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                number_of_seats = form.cleaned_data.get('number_of_seats')
                seats_class = form.cleaned_data.get('seats_class')
                meal = form.cleaned_data.get('meals')
                wheelchair = form.cleaned_data.get('wheelchair')
                stroller = form.cleaned_data.get('stroller')
                services = form.cleaned_data.get('services')
                lounge = form.cleaned_data.get('lounge')

                if is_valid_form([number_of_seats, round_trip]):
                    order.flight_seats(number_of_seats)
                    order.seats_class = seats_class
                    if order.seats_class == 'economy':
                        order.update_seats()
                    else:
                        order.update_seats_fc()

                    if meal == 'veg':
                        order.update_additional(10, number_of_seats)
                    elif meal == 'non-veg':
                        order.update_additional(12, number_of_seats)
                    elif meal == 'fruit':
                        order.update_additional(8, number_of_seats)
                    else:
                        None

                    if services == 'um':
                        order.update_additional(25, 1)

                    if lounge == 'yes':
                        if seats_class == 'economy':
                            order.update_additional(10, number_of_seats)
                        else:
                            # No additional charge if your ticket is a first class one
                            None

                    order.class_update()
                    order.flight_booked()
                    order.save()

                else:
                    messages.info(self.request, "Please fill in the required fields")


                #messages.success(self.request, "Almost Done")
                return redirect('core:discount')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")


# Details confirmation for round trip/ return flight
class round_trip(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        form = round_tripF()
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)
            context = {
                'object': order,
                'form': form
            }

            return render(self.request, "round_trip_search.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = round_tripF(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                from_place = form.cleaned_data.get('from_place')
                to_place = form.cleaned_data.get('to_place')
                number_of_seats = form.cleaned_data.get('number_of_seats')
                seats_class = form.cleaned_data.get('seats_class')
                start_date = form.cleaned_data.get('date')

                if is_valid_form([from_place, to_place, number_of_seats]):
                    if seats_class == 'first':
                        lookups = Q(start__icontains=from_place, destination__icontains=to_place, date=start_date,
                                    first_class_seats__gte=number_of_seats)

                    else:
                        lookups = Q(start__icontains=from_place, destination__icontains=to_place, date=start_date,
                                    number_seats_available__gte=number_of_seats)

                    results = FlightTicket.objects.filter(lookups)
                    context = {
                        'object_list' : results
                    }


                else:
                    messages.info(self.request, "Please fill in the required fields")


                #messages.success(self.request, "Almost Done")
                return render(self.request, 'flights_results.html', context)

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")



# Payment page
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
                    order.booked = True
                    order.save()

                else:
                    messages.info(self.request, "Please fill in the required fields")

                return redirect('core:booking_confirmed')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")


# Discount page
class discount_View(View):
    def get(self, *args, **kwargs):
        form = discount_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)
            context = {
                'object': order,
                'form': form
            }
            return render(self.request, "discount.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = discount_form(self.request.POST or None)
        try:
            order = Transactions.objects.get(user=self.request.user, booked=False)

            if form.is_valid():

                code = form.cleaned_data.get('code')

                if code == 'DISCOUNT25':
                    order.update_discount(25)

                else:
                    None

                return redirect('core:payment')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:home')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:home")


