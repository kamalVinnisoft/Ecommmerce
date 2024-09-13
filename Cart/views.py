from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.db.models import Count, F, FloatField, ExpressionWrapper,Sum
from django.db.models import Q
from Products.models import Product
from django.http import HttpResponseBadRequest, JsonResponse
from decimal import Decimal
# Create your views here.

class Cartview(View):
    def get(self, request):
        if request.user.is_authenticated:  # Check if the user is authenticated
            cart = Cart.objects.filter(user=request.user,remove=False)
            total_cost = cart.aggregate(
                total=Sum(F('product__discounted_price') * F('quantity'))
            )['total'] or 0
            
            return render(request, 'cart.html', {'cart': cart,"total_cost":total_cost})
        return render(request, 'cart.html')
    
    
# def Inc_ProductToCart(request):
#     if request.method == 'POST':
#         print(request.POST)
#         passs
    
def AddToCart(request):
    if request.method == 'POST':
        data = request.POST
        product_id= data.get('ProductId',None)
        quantity = data.get('quantity',1)
        if product_id:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.filter(product=product,user=request.user).first()
            if cart:
                cart.quantity += 1
                cart.total_cost = cart.total_cost + product.discounted_price
            else:
                cart = Cart.objects.create(product=product,user=request.user,total_cost= product.discounted_price,quantity=quantity)
            cart.save()
            
            total_cost = Cart.objects.filter(user=request.user).aggregate(
                total=Sum(F('product__discounted_price') * F('quantity'))
            )['total'] or 0
            
            cart_count = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            return JsonResponse({'message':f'{product.name} is added to your cart successfully.',"total_cost":total_cost,'cart_count':cart_count})
        else:
            return JsonResponse({'message':'product does not exist'})

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
            total_cost = Cart.objects.filter(user=request.user).aggregate(
                total=Sum(F('product__discounted_price') * F('quantity'))
            )['total'] or 0
            cart_count = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            return JsonResponse({'message':f'{product.name} is removed from your cart successfully.',"total_cost":total_cost,'cart_count':cart_count})
        else:
            return JsonResponse({'message':'product does not exist'})


def RemoveFromCart(request):
    if request.method == 'POST':
        data = request.POST
        product_id = data.get('ProductId', None)
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                # Remove product from cart
                Cart.objects.get(product=product, user=request.user).delete()
                
                # Calculate total cost after removing the product
                total_cost = Cart.objects.filter(user=request.user).aggregate(
                    total=Sum(F('product__discounted_price') * F('quantity'))
                )['total'] or 0  # Default to 0 if the cart is empty
                
                cart_count = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
                # Return success message and updated total cost
                return JsonResponse({
                    'message': f'{product.name} is removed from your cart successfully.',
                    'total_cost': total_cost,'cart_count':cart_count
                })
            except Product.DoesNotExist:
                # Product not found
                return JsonResponse({'message': 'Product does not exist.', 'total_cost': 0})
            except Cart.DoesNotExist:
                # Product not in cart
                return JsonResponse({'message': 'Product does not exist in your cart.', 'total_cost': 0})
        else:
            # Product ID is not provided
            return JsonResponse({'message': 'Product ID is missing.', 'total_cost': 0})


from django.http import JsonResponse

def UpdateCart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", request.POST)
        cart_data = {}
        
        for key, value in request.POST.items():
            if key.startswith('cart['):
                index, field = key[5:-1].split('][')
                if index not in cart_data:
                    cart_data[index] = {}
                cart_data[index][field] = value

        # Create or update Cart objects
   
        for item in cart_data.values():
            product_id = item.get('productId')
            quantity = item.get('quantity')

            if product_id and quantity and int(quantity) > 0:
                product = Product.objects.filter(id=product_id).first()

                if product:
                    cart = Cart.objects.filter(product=product,
                        user=request.user).first()
                    if cart:
                        cart.quantity=cart.quantity + int(quantity)
                        cart.total_cost = product.discounted_price * int(cart.quantity + int(quantity))
                    else:
                        cart= Cart.objects.create(
                            product=product,
                            user=request.user,total_cost= product.discounted_price * int(quantity),quantity=quantity
                        )
                    cart.save()

        # Return the updated cart data as a response
        return JsonResponse({
            'status': 'success',
            'message': 'Cart updated successfully',
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated or invalid request method'})

    