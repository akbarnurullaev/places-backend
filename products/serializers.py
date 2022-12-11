from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('place',)


class ProductSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Product
        exclude = ('category',)
