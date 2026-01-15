from rest_framework import generics
from rest_framework.response import Response

class OrderListView(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "Orders list - WIP"})

class OrderCreateView(generics.CreateAPIView):
    def post(self, request):
        return Response({"message": "Order create - WIP"})
