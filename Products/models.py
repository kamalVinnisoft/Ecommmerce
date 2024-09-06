from django.db import models
from utility.models import BaseModel
from django.core.exceptions import ValidationError

class Category(BaseModel):
    name= models.CharField(max_length=255, db_index=True)
    def __str__(self):
        return self.name 
    
class Product(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    MainImage = models.ImageField(upload_to='media/', blank=True, null=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    def clean(self):
        if self.price < 0:
            raise ValidationError('Price cannot be negative')
        if self.discounted_price < 0:
            raise ValidationError('Discounted Price cannot be negative')
        if self.discounted_price > self.price:
            raise ValidationError('Discounted Price cannot exceed the regular price')

    def is_in_current_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    image = models.ImageField(upload_to='media/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return f"Image for {self.product.name}"

