from django.urls import path
from . import views


app_name = 'kitchen_management'

urlpatterns = [
    path('kitchen_section/<int:kitchen_section_id>/', views.kitchen_section_orders_view, name="kitchen_section"),
    path('send_msg/<int:kitchen_section_id>/', views.send_msg, name="send_msg"),
]