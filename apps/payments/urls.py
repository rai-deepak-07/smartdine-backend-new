from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/pay/', views.restaurant_payment, name='restaurant_pay'),
]
