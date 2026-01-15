from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path('list/', views.MenuListView.as_view(), name='list'),
]
