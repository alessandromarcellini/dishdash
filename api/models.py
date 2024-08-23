from django.db import models
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()

    #tags = models.ManyToManyField() #TODO: create a tag model to specify the type of restaurant (italian, indian, fish, meat...)

    def __str__(self):
        return f"RESTAURANT: {self.name}"

class Table(models.Model):
    number = models.IntegerField()
    showing = models.BooleanField(default=True) #optimization, won't need to check if there's an order pending (not fullfilled)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"TABLE: {self.number} ({self.restaurant})"

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        restaurant_tables = Table.objects.filter(restaurant=self.restaurant, number=self.number).exclude(id=self.id)
        if restaurant_tables:
            raise ValidationError("Table number must be unique for the restaurant.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



class Reservation(models.Model):
    customer_name = models.CharField(max_length=256)
    date_time = models.DateTimeField()
    number_of_people = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    fullfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"RESERVATION: {self.customer_name}, {self.table}"

class RestaurantSection(models.Model):
    name = models.CharField(max_length=256)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    #TODO: add kitchen components

    def __str__(self):
        return f"RESTAURANT SECTION: {self.name}"

#-------------------------------#-------------------------------#-------------------------------#-------------------------------

class Allergen(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"ALLERGEN: {self.name}"

class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    allergens = models.ManyToManyField(Allergen, blank=True)

    def __str__(self):
        return f"INGREDIENT: {self.name}"

class MenuSection(models.Model):
    name = models.CharField(max_length=256)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    #TODO: should it refer to a specific restaurant?

    def __str__(self):
        return f"MENU SECTION: {self.name}"

class Dish(models.Model):
    name = models.CharField(max_length=256)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    cost = models.FloatField()
    is_available = models.BooleanField(default=True)  # displayed on the menu and on the waiter's page

    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE) #TODO: diplay only the user's restaurant's sections
    restaurant_section = models.ForeignKey(RestaurantSection, on_delete=models.SET_NULL, null=True, validators=[]) #TODO: diplay only the user's restaurant's sections

    def __str__(self):
        return f"DISH: {self.name} {self.restaurant_section.restaurant}"


    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.menu_section and self.restaurant_section:
            if self.menu_section.restaurant != self.restaurant_section.restaurant:
                raise ValidationError("Menu section and Restaurant section aren't from the same restaurant.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Dish, self).save(*args, **kwargs)

class OrderItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.dish}"

class Order(models.Model):
    #TODO: waiter = models.ForeignKey(Waiter)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    dishes = models.ManyToManyField(OrderItem, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    takeaway = models.BooleanField(default=False)
    fullfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"ORDER: {self.table}, {self.date_time}"

    def clean(self):
        if self.takeaway and self.table is not None:
            raise ValidationError("For takeaway orders, table must be null.")
        if not self.takeaway and self.table is None:
            raise ValidationError("For non-takeaway orders, table must not be null.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        for item in self.dishes.all():
            item.delete()
        super(Order, self).delete()








