from django.urls import path
from .consumers import KitchenManagementConsumer


websocket_urlpatterns = [
    path('ws/<int:kitchen_section_id>/', KitchenManagementConsumer.as_asgi()),
]