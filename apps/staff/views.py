from rest_framework import generics
from rest_framework.response import Response

class StaffListView(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "Staff list - WIP"})
