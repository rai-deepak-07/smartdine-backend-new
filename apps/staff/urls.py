from django.urls import path
from . import views

app_name = 'staff'
urlpatterns = [
    path('list/', views.StaffListView.as_view(), name='list'),
]
