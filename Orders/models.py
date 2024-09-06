from django.db import models
from Products.models import *
from Users.models import *
from utility.models import BaseModel


# Create your models here.

from django.db import models
from django.conf import settings  # To get the user model

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relating to CustomUser
    full_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)  # Optional
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Optional phone number
    default = models.BooleanField(default=False)  # Marks as default shipping address

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}, {self.street_address}, {self.city}, {self.country}"

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    
# class order(BaseModel):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     user =models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    