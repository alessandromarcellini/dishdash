from django.urls import path
from . import views



app_name = 'waiters'

urlpatterns = [
    path('', views.waiter_initial_view, name="waiter_initial"),
    path('new_order/<int:table_id>/', views.new_order_view, name="new_order"),
]