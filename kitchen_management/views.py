from django.shortcuts import render, get_object_or_404
from asgiref.sync import async_to_sync

from api.models import RestaurantSection, Order

from channels.layers import get_channel_layer

def kitchen_section_orders_view(request, kitchen_section_id):
    #TODO: check if user works in this section
    context = {}

    kitchen_section = get_object_or_404(RestaurantSection, id=kitchen_section_id)
    context["kitchen_section"] = kitchen_section

    #get all orders having the kitchen_section in it
    orders_to_display = Order.objects.filter(dishes__dish__restaurant_section__id=kitchen_section_id, fullfilled=False).distinct()
    context["orders_to_display"] = orders_to_display
    context["user"] = request.user

    #get the current orders of this kitchen section
    #orders_to_display = Order.objects.filter(restaurant_sections)


    return render(request, 'kitchen_management/kitchen_section.html', context)



def send_msg(request, kitchen_section_id):
    context = {}

    context["user"] = request.user
    context["kitchen_section"] = get_object_or_404(RestaurantSection, id=kitchen_section_id)

    layer = get_channel_layer()

    async_to_sync(layer.group_send)(
        f"kitchen-{kitchen_section_id}",
        {
            "type": "kitchen_section_message",
            "message": "testing...",
            "sender": request.user.username,
        }
    )

    return render(request, 'kitchen_management/send_message.html', context)