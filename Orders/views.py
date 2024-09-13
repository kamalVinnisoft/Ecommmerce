from typing import Any
from django.http import HttpRequest,JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from Cart.models import *
from django.db.models import Sum
from django.db import transaction
import json
# Create your views here.



class Checkout(View):
    def dispatch(self, request, *args: Any, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))  
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        cart = Cart.objects.filter(user=request.user)
        total_cost = cart.aggregate(total=Sum('total_cost'))['total']
        
        shipping_address = ShippingAddress.objects.filter(user=request.user,default=True).first()
        
        return render(request,'checkout.html',{'shipping_address':shipping_address,'cart':cart,'total_cost':total_cost})
    
    def post(self, request):
        data = request.POST
        if 'shipping_address' in data:
            first_name = data.get('firstName', None)
            last_name = data.get('lastName', None)
            street_address = data.get('address1', None)
            apartment_address = data.get('address2', None)  # Ensure field names match the form
            city = data.get('city', None)
            state = data.get('state', None)
            country = data.get('country', None)
            phone_number = data.get('mobile', None)
            email = data.get('email', None)
            postal_code = data.get('zipcode', None)

            # Ensure required fields are not None or empty
            if not all([first_name, last_name, street_address, city, state, country, phone_number, postal_code]):
                return render_with_messages(request, 'checkout.html', {'error_message': "All fields except apartment address are required."})

            # Create the ShippingAddress object
            shipping_address, created = ShippingAddress.objects.update_or_create(
            user=request.user,  # Fields used to check if the record already exists
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'city': city,
                'state': state,
                'country': country,
                'phone_number': phone_number,
                'email': email,
                'postal_code': postal_code
                }
            )
            return render_with_messages(request, 'checkout.html', {'success_message': "Shipping Address created Successfully.",'shipping_address':shipping_address})
        elif 'place_order' in data:
            print(data)
            user = request.user
            cart_items = Cart.objects.filter(user=user,remove=False)
            shipping_address = ShippingAddress.objects.filter(user=user).values().first()
            shipping_address.pop('created_at','')
            shipping_address.pop('updated_at','')
            shipping_address_json = json.dumps(shipping_address)
            print(shipping_address_json)
            # print(shipping_address)
            total_cost = cart_items.aggregate(total=Sum('total_cost'))['total'] or 0
            
            # Ensure there is a shipping address and items in the cart
            if not shipping_address:
                return render_with_messages(request, 'checkout.html', error_message= "Shipping address not found")
    
            if int(total_cost) <= 0:
                print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                return render_with_messages(request, 'checkout.html', error_message= "Cart is empty or invalid")
    
            # Create the order
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    shipping_address=shipping_address_json,
                    total_cost=total_cost,
                    status='pending'  # Default to 'pending' status
                )
        
                # Add cart items to the order (assuming you have a many-to-many field)s
                order.items.set(cart_items)
                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                order.save()
                print(">>>>>>>>>>fffffffff",order.items.all())
                # Clear the cart after the order is created
                for item in cart_items:
                    print("Marking item as deleted:", item.id)
                    item.remove = True
                    item.save()
                    
                # Debugging information after marking items as deleted
                print("Updated order items:", order.items.all())
        
            # Respond with success
            return render_with_messages(request, 'orders.html', {'success_message': 'Order created successfully'})
    

class OrdersList(View):
    def dispatch(self, request, *args: Any, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))  
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        order = Order.objects.filter(user=request.user)
        keys_to_remove = ['id','is_deleted','user_id','default']
       # Keys to remove from the shipping address
        keys_to_remove = ['id', 'is_deleted', 'user_id', 'default']

        for ord in order:
            # Load the shipping address from JSON string
            shipping_address = json.loads(ord.shipping_address)
            
            # Remove specified keys if they exist
            for key in keys_to_remove:
                shipping_address.pop(key, None)  # Provide a default value of None to avoid KeyError
            
            # Update the order's shipping_address field
            ord.shipping_address = shipping_address
            total_cost = order.aggregate(total=Sum('total_cost'))['total']
        return render(request,'orders.html',{'order':order,'total_cost':total_cost})
    



        
        
        