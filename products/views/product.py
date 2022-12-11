from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import JSONParser

from places.models import Place

from products.serializers import ProductSerializer

from products.models import Category, Product


class ProductsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, place_id, category_id, format=None):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)

    def post(self, request, place_id, category_id, format=None):
        category = Category.objects.get(pk=category_id)

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)

        return Response(serializer.data)


class ProductsDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self, place_id, category_id, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, place_id, category_id, product_id, format=None):
        product = self.get_object(product_id, place_id, category_id)
        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def put(self, request, place_id, category_id, product_id, format=None):
        product = self.get_object(product_id, place_id, category_id)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, place_id, category_id, format=None):
        product = self.get_object(category_id, place_id)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
