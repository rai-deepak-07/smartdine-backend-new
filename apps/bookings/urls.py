# apps/bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('list/', views.BookingListView.as_view(), name='list'),
    path('create/', views.BookingCreateView.as_view(), name='create'),
]
