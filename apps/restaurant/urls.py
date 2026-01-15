from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('register/', views.RestaurantRegisterView.as_view(), name='register'),
    path('list/', views.RestaurantListView.as_view(), name='list'),
    path('<str:pk>/', views.RestaurantDetailView.as_view(), name='detail'),
]

