from django.urls import path 
from .views import home_v, destination, pricing, contact ,ticket_list, destination_details_V,flights, seats, my_account, my_flights, flight_details_V, add_to_cart,confirmation, payment_View

app_name = 'core'

urlpatterns= [
    path('', home_v, name='home'),
    path('index.html', home_v, name='home'),
    path('destination.html', destination, name='destination'),
    path('pricing.html', pricing, name='pricing'),
    path('contact.html', contact, name='contact'),
    path('ticket_list.html', ticket_list, name='ticket-list'),
    path('flights_results.html', flights , name='flights'),
    path('seats.html', seats, name='seats'),
    path('flight_details/<slug>/', flight_details_V, name='flight_details'),
    path('destination_details/<slug>/', destination_details_V, name='destination_details'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('confirmation', confirmation.as_view(), name='confirmation'),
    path('payment', payment_View.as_view(), name='payment'),
    path('my_account', my_account, name='my_account'),
    path('my_flights', my_flights, name='my_flights'),
]