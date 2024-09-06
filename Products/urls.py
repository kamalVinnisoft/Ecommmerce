from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(),name="home"),
    path('shop/',Shop.as_view(),name="shop"),
    path('product/<int:id>/',ProductDetail.as_view(), name='product-detail'),

]