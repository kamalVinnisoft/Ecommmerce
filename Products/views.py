from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.


class Home(View):
    def get(self,request):
        latest_products = Product.objects.all().order_by('-id')[:15]
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
    def get(self, request):
        # Get search query and category filter from request
        q = request.GET.get('q', None)
        category_id = request.GET.get('category', None)
        price_ranges = request.GET.getlist('price', [])
        print("Selected price ranges:", price_ranges)
        
        # Start with all products
        products_list = Product.objects.all()

        # Apply search query filtering
        if q:
            categories = Category.objects.filter(name__icontains=q).values_list('id', flat=True)
            products_list = products_list.filter(Q(name__icontains=q) | Q(category_id__in=categories))
        
        # Apply category filter if specified
        if category_id:
            products_list = products_list.filter(category_id=category_id)
        prod_list=[]
        # Apply price range filters
        if price_ranges and 'all' not in price_ranges:
            
            for price_range in price_ranges:
                # try:
                min_price, max_price = map(int, price_range.split('-'))
                print(min_price, max_price)
                product_list = products_list.filter(Q(discounted_price__gte=min_price, discounted_price__lte=max_price))
                prod_list.extend(product_list)
            products_list = prod_list
            
        # Paginate the filtered queryset
        paginator = Paginator(products_list, 4)  # Show 4 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,  # Pass the paginated products
            'q': q,  # Pass the search term back to the template
            'category_id': category_id,  # Pass the selected category ID
            'categories': Category.objects.all(),  # Pass all categories for filtering
            'price':price_ranges
        }
        return render(request, 'shop.html', context=context)


class ProductDetail(View):
    def get(self, request, id):
        product = Product.objects.filter(id=id).first()
        similar_products = Product.objects.filter(category=product.category)
        context = {
            'product': product,
            'similar_products':similar_products,
        }
        
        return render(request, 'detail.html', context)
    

        