from rest_framework import serializers
from .models import *

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantSection
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

