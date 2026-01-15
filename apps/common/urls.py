from django.urls import path
from . import views

app_name = 'common'
urlpatterns = [
    path('status/', views.StatusView.as_view(), name='status'),
]
