from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    #RESTAURANTS
    path('v1/restaurants/', views.get_restaurants_response, name="restaurants"),
    path('v1/restaurant/<int:restaurant_id>/tables/', views.get_restaurant_tables_response, name="restaurant_tables"),
    path('v1/restaurant/<int:restaurant_id>/available_tables/', views.get_available_tables_response, name="available_tables"),
    path('v1/restaurant/<int:restaurant_id>/current_orders/', views.get_current_orders_response, name="current_orders"),
    path('v1/restaurant/<int:restaurant_id>/kitchen_sections/', views.get_restaurant_sections_response, name="restaurant_sections"),
    path('v1/restaurant/<int:restaurant_id>/', views.get_restaurant_response, name="restaurant"),
    path('v1/restaurant/<int:restaurant_id>/menu/', views.get_menu_response, name="menu"),
    path('v1/restaurant/<int:restaurant_id>/current_reservations/', views.get_current_reservations, name="current_reservation"),

    #DISHES
    path('v1/dish/<int:dish_id>/allergens/', views.get_dish_allergens_response, name="dish_allergens"),

    # GENERAL
    path('v1/tables/', views.get_tables_response, name="tables"),

    #ORDERITEMS
    path('v1/items/update/<int:item_id>/', views.update_item_status, name="update_item_status")
]