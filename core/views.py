from django.shortcuts import render

# Create your views here.

def home_v(request):
    return render(request, "index.html")

def destination(request):
    return render(request, "destination.html")

def pricing(request):
    return render(request, "pricing.html")

def contact(request):
    return render(request, "contact.html")