from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from back.models import *
from myauth.models import *

def home(request):
    #return HttpResponse("<h1>Bienvenu sur notre site!</h1>")
    #categories = Category.objects.filter(active=True).order_by('name') 
    products = Product.objects.filter(active=True).order_by('name')[:12]
    arrivals = Arrival.objects.filter(closed=False)
    arrivals_details = []
    for arrival in arrivals:
        arrivals_details += list(Arrival_details.objects.filter(arrival=arrival))
    context = {
        #'categories': categories,
        'products': products,
        'arrivals_details': arrivals_details
    }
    return render(request, 'front/index.html', context)

def shop(request):
    return render(request, 'front/shop.html')

def cart(request):
    return render(request, 'front/cart.html')

def detail(request):
    return render(request, 'front/detail.html')

def checkout(request):
    return render(request, 'front/checkout.html')

def contact(request):
    return render(request, 'front/contact.html')