from django.urls import path
from .views import SignUp,Login

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/',Login.as_view(),name="login")
]