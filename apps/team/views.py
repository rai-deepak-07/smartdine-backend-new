from rest_framework import generics
from rest_framework.response import Response

class TeamListView(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "Team list - WIP"})
