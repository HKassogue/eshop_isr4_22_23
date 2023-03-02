from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    #return HttpResponse("<h1>Bienvenu sur notre site!</h1>")
    return render(request, 'front/index.html')

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