from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # path('login/', views.UniversalLoginView.as_view(), name='login'),
    path('profile/', views.CompleteUserProfileView.as_view(), name='profile'),
    path('verify-email/<uidb64>/<token>/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]

