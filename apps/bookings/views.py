from rest_framework import generics
from rest_framework.response import Response

class BookingListView(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "Bookings list - WIP"})

class BookingCreateView(generics.CreateAPIView):
    def post(self, request):
        return Response({"message": "Booking create - WIP"})
