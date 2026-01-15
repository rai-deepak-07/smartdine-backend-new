from django.urls import path
from . import views

app_name = 'team'
urlpatterns = [
    path('list/', views.TeamListView.as_view(), name='list'),
]
