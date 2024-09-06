from django.db import models
from Products.models import Product
from Users.models import *
from utility.models import BaseModel


# Create your models here.
class Cart(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user =models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
