from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import JSONParser

from places.serializers import PlaceSerializer

from .models import Place


class PlacesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, format=None):
        queryset = Place.objects.all()
        serializer = PlaceSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data)


class PlacesDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self, place_url):
        try:
            return Place.objects.get(url=place_url)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, place_url, format=None):
        place = self.get_object(place_url)
        serializer = PlaceSerializer(place)

        return Response(serializer.data)

    def put(self, request, place_url, format=None):
        place = self.get_object(place_url)
        serializer = PlaceSerializer(place, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, place_url, format=None):
        transformer = self.get_object(place_url)
        transformer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
