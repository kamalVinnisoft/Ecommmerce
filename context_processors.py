from Products.models import Category
from Cart.models import Cart
from django.db.models import Sum

def CategoryList(request):
    category = Category.objects.all()

    return {
        'category': category
    }

def CartCount(request):
    try:
        cart_count = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print(cart_count)
        return {
            'cart_count': cart_count
        }
    except:
        return {}