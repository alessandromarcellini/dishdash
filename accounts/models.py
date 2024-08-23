from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from api.models import Restaurant, RestaurantSection

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('kitchen_member', 'Kitchen Member'), #staff member that can view his kitchen status
        ('waiter', 'Waiter'),
        ('restaurant_admin', 'Restaurant Admin'),
        ('user', 'User')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, blank=True, null=True)
    kitchen = models.ForeignKey(RestaurantSection, on_delete=models.SET_NULL, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def clean(self):
        if self.role == 'user' and self.restaurant:
            raise ValidationError("Staff users must be assigned to a restaurant.")
        elif self.role != 'user' and not self.restaurant:
            raise ValidationError("Staff members must be assigned to a restaurant")
        elif self.role == 'kitchen_member' and not self.kitchen:
            raise ValidationError("Kitchen members must be assigned to a kitchen.")
        elif self.role == 'kitchen_member' and self.restaurant != self.kitchen.restaurant:
            raise ValidationError("Kitchen must be from the same restaurant as the user.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
