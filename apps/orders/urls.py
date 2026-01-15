from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('list/', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
]
