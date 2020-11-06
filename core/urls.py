from django.urls import path 
from .views import home_v, destination, pricing, contact

app_name = 'core'

urlpatterns= [
    path('', home_v, name='home'),
    path('index.html', home_v, name='home'),
    path('destination.html', destination, name='destination'),
    path('pricing.html', pricing, name='pricing'),
    path('contact.html', contact, name='contact')
]