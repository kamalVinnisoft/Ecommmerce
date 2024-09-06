from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.db.models import Q
from Products.models import Product
from django.http import HttpResponseBadRequest, JsonResponse
# Create your views here.

class Cartview(View):
    def get(self, request):
        if request.user.is_authenticated:  # Check if the user is authenticated
            cart = Cart.objects.filter(user=request.user)
            return render(request, 'cart.html', {'cart': cart})
        return render(request, 'cart.html')
    
    
# def Inc_ProductToCart(request):
#     if request.method == 'POST':
#         print(request.POST)
#         passs
    
def AddToCart(request):
    if request.method == 'POST':
        data = request.POST
        product_id= data.get('ProductId',None)
        if product_id:
            product = Product.objects.get(id=product_id)
            print("llllllllllllllllllllllllllllllll",product)
            cart = Cart.objects.filter(product=product,user=request.user).first()
            print("..............................",cart)
            if cart:
                cart.quantity += 1
                cart.total_cost = cart.total_cost + product.discounted_price
            else:
                cart = Cart.objects.create(product=product,user=request.user,total_cost= product.discounted_price)
            cart.save()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",cart.quantity)
            return JsonResponse({'msg':f'{product.name} is added to your cart successfully.'})
        else:
            return JsonResponse({'msg':'product does not exist'})

def DecreaseFromCart(request):
    if request.method == 'POST':
        data = request.POST
        product_id= data.get('ProductId',None)
        if product_id:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.filter(product=product,user=request.user).first()
            if cart:
                cart.quantity -= 1
                cart.total_cost = cart.total_cost - product.discounted_price
            else:
                return JsonResponse()
            cart.save()
            return JsonResponse({'msg':f'{product.name} is removed from your cart successfully.'})
        else:
            return JsonResponse({'msg':'product does not exist'})


def RemoveFromCart(request):
    if request.method == 'POST':
        data = request.POST
        product_id= data.get('ProductId',None)
        if product_id:
            product = Product.objects.get(id=product_id)
            try:
                cart = Cart.objects.get(product=product,user=request.user).delete()
                return JsonResponse({'msg':f'{product.name} is removed from your cart successfully.'})
            except:
                return JsonResponse({'msg':'product does not exist in your cart.'})
        else:
            return JsonResponse({'msg':'product does not exist in your cart.'})