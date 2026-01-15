from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Restaurant
from .serializers import RestaurantSerializer, RestaurantCreateSerializer
from apps.geo.models import State, City

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.filter(is_visible_to_users=True).select_related('city__state')
    serializer_class = RestaurantSerializer

class RestaurantRegisterView(generics.CreateAPIView):
    serializer_class = RestaurantCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'states': State.objects.all(),
            'cities': City.objects.all()
        })
        return context

class RestaurantFormDataView(generics.GenericAPIView):
    def get(self, request):
        return Response({
            'states': [{'id': s.id, 'name': s.name} for s in State.objects.all()],
            'cities': [{'id': c.id, 'name': c.name, 'state': c.state.id} for c in City.objects.all()]
        })


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'
