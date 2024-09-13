import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],  # Filter by product name (case-insensitive)
            'category__name': ['iexact'],  # Filter by category name
        }
    
