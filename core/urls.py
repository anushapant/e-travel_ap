from django.urls import path 
from .views import home_v, destination, pricing, contact, ticket_list, flights, seats, flight_details_V

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
    path('flight_details/<slug>/', flight_details_V.as_view(), name='flight_details')
]