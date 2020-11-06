from django.shortcuts import render

# Create your views here.

def home_v(request):
    return render(request, "index.html")