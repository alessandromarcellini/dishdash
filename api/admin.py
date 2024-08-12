from django.contrib import admin

from . import models


class TableAdmin(admin.ModelAdmin):
    ordering = ['restaurant', 'number']

class RestaurantAdmin(admin.ModelAdmin):
    ordering = ['name']

class OrderAdmin(admin.ModelAdmin):
    ordering = ['table', 'date_time']

class ReservationAdmin(admin.ModelAdmin):
    ordering = ['table', 'date_time', 'customer_name']

class RestaurantSectionAdmin(admin.ModelAdmin):
    ordering = ['restaurant']

class MenuSectionAdmin(admin.ModelAdmin):
    ordering = ['restaurant', 'name']

class DishAdmin(admin.ModelAdmin):
    ordering = ['menu_section', 'name']





admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Table, TableAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Reservation, ReservationAdmin)
admin.site.register(models.RestaurantSection, RestaurantSectionAdmin)
admin.site.register(models.Allergen)
admin.site.register(models.Ingredient)
admin.site.register(models.MenuSection, MenuSectionAdmin)
admin.site.register(models.Dish, DishAdmin)
