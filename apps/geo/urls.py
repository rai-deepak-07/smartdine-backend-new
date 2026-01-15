from django.urls import path
from . import views

app_name = 'geo'

urlpatterns = [
    path('states/', views.StateListView.as_view(), name='states'),
    path('cities/<int:state_id>/', views.CityListView.as_view(), name='cities'),
]
