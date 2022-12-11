from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Place
        fields = ['id', 'name', 'url', 'currency', 'main_language', 'phone',
                  'wifi_password', 'address', 'additional_info', 'theme', 'logo', 'cover']
