from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import JSONParser

from places.models import Place

from products.serializers import CategorySerializer

from products.models import Category


class CategoriesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, place_url, format=None):
        queryset = Category.objects.filter(place__url=place_url)
        serializer = CategorySerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)

    def post(self, request, place_url, format=None):
        place = Place.objects.get(url=place_url)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(place=place)

        return Response(serializer.data)


class CategoriesDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser,)

    def get_object(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, place_url, category_id, format=None):
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def put(self, request, place_url, category_id, format=None):
        category = self.get_object(category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, place_url, category_id, format=None):
        category = self.get_object(category_id)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
