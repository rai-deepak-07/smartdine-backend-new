from rest_framework import generics
from .serializers import StateSerializer, CitySerializer
from .models import State, City

class StateListView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    def get_queryset(self):
        state_id = self.kwargs['state_id']
        return City.objects.filter(state_id=state_id)
