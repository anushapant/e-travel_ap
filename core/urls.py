from django.urls import path 
from .views import home_v

urlpatterns= [
    path('', home_v.as_view(), name='home'),
]