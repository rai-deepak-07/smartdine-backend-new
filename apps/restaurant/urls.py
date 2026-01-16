from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('register/', views.RestaurantRegisterView.as_view(), name='register'),
    path('list/', views.RestaurantListView.as_view(), name='list'),
    path('owner/profile/', views.RestaurantOwnerProfileView.as_view(), name='owner-profile'),
    path('<str:id>/', views.RestaurantDetailView.as_view(), name='detail'),
]

