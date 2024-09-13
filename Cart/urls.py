from django.urls import path
from .views import *

urlpatterns = [
    path('',Cartview.as_view(),name="cart"),
    path('addtocart/',AddToCart,name="addtocart"),
    path('removefromcart/',RemoveFromCart,name="removefromcart"),
    path('decreasefromCart/',DecreaseFromCart,name='decreasefromCart'),
    path('updateCart/',UpdateCart,name='updateCart'),
   
]