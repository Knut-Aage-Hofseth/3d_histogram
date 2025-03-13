# appname/views.py
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {
        'title': 'Map of Oslo with inhabitants'
    }
    return render(request, 'kart.html', context)

def about(request):
    return HttpResponse("This is the about page")