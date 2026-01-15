from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import MockPayment
from apps.restaurant.models import Restaurant
from django.utils import timezone
from decimal import Decimal

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurant_payment(request):
    """Dummy payment - Sets restaurant annual_fee_status to 'paid'"""
    restaurant_id = request.data.get('restaurant_id')
    
    if not restaurant_id:
        return Response({"error": "restaurant_id required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify restaurant belongs to logged-in owner
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=request.user)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found or access denied"}, status=status.HTTP_403_FORBIDDEN)
    
    # Create payment record
    transaction_id = f"txn_{restaurant_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    payment = MockPayment.objects.create(
        restaurant=restaurant,
        amount=Decimal('999.00'),
        status='completed',
        transaction_id=transaction_id
    )
    
    # ✅ UPDATE RESTAURANT TO PAID & VISIBLE
    restaurant.annual_fee_status = 'paid'
    restaurant.is_visible_to_users = True
    restaurant.fee_due_date = timezone.now() + timezone.timedelta(days=365)
    restaurant.save()
    
    return Response({
        "success": True,
        "message": "✅ Annual fee ₹999 paid! Your restaurant is now LIVE for customers!",
        "payment": {
            "id": payment.id,
            "amount": "₹999.00",
            "transaction_id": payment.transaction_id,
            "status": payment.status
        },
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.res_name,
            "status": restaurant.annual_fee_status,
            "visible": restaurant.is_visible_to_users
        }
    }, status=status.HTTP_200_OK)
