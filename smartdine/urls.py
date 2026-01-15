from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/restaurant/', include('apps.restaurant.urls')),
    path('api/v1/geo/', include('apps.geo.urls')),
    # path('api/v1/bookings/', include('apps.bookings.urls')),  # COMMENTED OUT
    # path('api/v1/orders/', include('apps.orders.urls')),  # COMMENTED OUT
    path('api/v1/payments/', include('apps.payments.urls')),
    

    # JWT Authentication
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
