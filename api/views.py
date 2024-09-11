from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import *


@api_view(['GET'])
def get_tables_response(request):
    to_pass = Table.objects.all()
    serializer = TableSerializer(to_pass, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def post_tables_view(request):
#     to_add = request.data
#     serializer = TableSerializer(data=to_add)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)



@api_view(['GET'])
def get_restaurant_tables_response(request, restaurant_id):
    tables = Table.objects.filter(restaurant_id=restaurant_id)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_available_tables_response(request, restaurant_id):
    available_tables = Table.objects.filter(restaurant_id=restaurant_id, is_available=True)
    serializer = TableSerializer(available_tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_dish_allergens_response(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    ingredients = dish.ingredients.all()
    allergens = []
    for ingredient in ingredients:
        allergens.extend(list(ingredient.allergens.all()))
    serializer = AllergenSerializer(allergens, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_current_orders_response(request, restaurant_id):
    orders = Order.objects.filter(table__restaurant_id=restaurant_id, fullfilled=False)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_restaurant_sections_response(request, restaurant_id):
    sections = RestaurantSection.objects.filter(restaurant_id=restaurant_id)
    serializer = SectionSerializer(sections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_restaurants_response(request):
    restaurant = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurant, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_restaurant_response(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    serializer = RestaurantSerializer(restaurant, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_menu_response(request, restaurant_id):
    menu = Dish.objects.filter(restaurant_section__restaurant_id=restaurant_id)
    serializer = MenuSerializer(menu, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_current_reservations(request, restaurant_id):
    reservations = Reservation.objects.filter(table__restaurant_id=restaurant_id, fullfilled=False)
    serializer = ReservationSerializer(reservations, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def update_item_status(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    serializer = UpdateOrderItemStatusSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)




#TODO: get_reservations with a specific date








