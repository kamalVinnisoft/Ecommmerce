from django.urls import path
from .views import *

urlpatterns = [
    path('',Checkout.as_view(),name="checkout"),
    path('orders-listing/',OrdersList.as_view(),name="orders-listing"),
    # path('product/<int:id>/',ProductDetail.as_view(), name='product-detail'),

]