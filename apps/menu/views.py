from rest_framework import generics
from rest_framework.response import Response

class MenuListView(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "Menu list - WIP"})
