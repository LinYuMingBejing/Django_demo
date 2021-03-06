from api.models import Restaurant
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'restaurant',
            'ratings',
            'price',
            'types',
            'areas',
        ]

 