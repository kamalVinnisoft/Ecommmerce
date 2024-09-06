from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.db.models import Q
# Create your views here.




class Home(View):
    def get(self,request):
        latest_products = Product.objects.all().order_by('-id')[:8]
        print(">>>>>",latest_products)
        trendy_products = (Product.objects
                       .annotate(
                           turnover=ExpressionWrapper(
                               F('stock') - F('current_stock'),
                               output_field=FloatField()
                           )
                       )
                       .filter(turnover__gt=0)
                       .order_by('-turnover'))
        print(">>>>>>>>>>>>>>>>>>>>>>>>",trendy_products) 
        context={
            'latest_products':latest_products,
            'trendy_products':trendy_products
        }
        return render(request,'index.html',context=context)



class Shop(View):
    def get(self,request):
        q = request.GET.get('q',None)
        products = Product.objects.all()
        print("]]]]]]",products)
        if q:
            print("::::")
            # Filter categories based on the query
            categories = Category.objects.filter(name__icontains=q).values_list('id',flat=True)

            # Filter products based on the query
            products = Product.objects.filter(Q(name__icontains=q) | Q(category_id__in=categories))
            print(":::::",products)
       
        context={
            'products':products,
            
        }
        return render(request,'shop.html',context=context)

class ProductDetail(View):
    def get(self, request, id):
        product = Product.objects.filter(id=id).first()
        print(">>>>>>>>>>>>..",product)
        similar_products = Product.objects.filter(category=product.category)
        print(">>>>>>>>>>>>>>>",similar_products)
        context = {
            'product': product,
            'similar_products':similar_products,
        }
        
        return render(request, 'detail.html', context)
    

        