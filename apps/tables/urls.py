from django.urls import path
from . import views

app_name = 'tables'
urlpatterns = [
    path('list/', views.TableListView.as_view(), name='list'),
]
