from django.shortcuts import render, HttpResponse, get_object_or_404
from api.models import Table, Dish, Order, MenuSection, OrderItem

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .forms import OrderItemForm


def waiter_initial_view(request):
    user = request.user
    if user.role != 'waiter':
        return HttpResponse("Only waiters can access this page.")
    context = {}
    tables_to_display = Table.objects.filter(restaurant=user.restaurant)
    context["tables_to_display"] = tables_to_display

    return render(request, 'waiters/waiter_initial.html', context)


def new_order_view(request, table_id):
    def update_order(current_order):
        form = OrderItemForm(request.POST, user=user)
        if form.is_valid():
            if not current_order:
                # create it
                current_order = Order.objects.create(table=table)
                current_order.save()

            quantity = int(form.cleaned_data['quantity'])
            dish = Dish.objects.get(id=int(form.cleaned_data['dish']))
            item = OrderItem.objects.create(dish=dish, quantity=quantity)
            item.save()
            current_order.dishes.add(item)
        else:
            return HttpResponse("Something went wrong with your form.")
        return current_order, item
    # ---------------------------------------------

    def send_changes(item: OrderItem, user, current_order, table):
        # TODO: send infos in the admin WebSocket

        serialized_item = {
            'quantity': item.quantity,
            'dish_name': item.dish.name,
            'is_dish_done': item.is_done,
            'order_id': current_order.id,
            'table_number': table.number,
        }

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            f"kitchen-{item.dish.restaurant_section.id}",
            {
                'type': 'kitchen_section_message',
                'sender': user.email,
                'data': serialized_item,
            }
        )


    #---------------------------------------------


    table = get_object_or_404(Table, id=table_id)
    user = request.user
    if not user.is_authenticated or user.role != 'waiter' or user.restaurant != table.restaurant:
        return HttpResponse(f"Only waiters of {table.restaurant.name} can access this page.")
    context = {}
    context["table"] = table
    #getting dishes from menu_sections in order to display them ordered by section
    menu_sections = MenuSection.objects.filter(restaurant=user.restaurant)
    dishes_to_select = []
    for menu_section in menu_sections.all():
        dishes_to_select.extend(list(Dish.objects.filter(menu_section=menu_section)))
    context["dishes_to_select"] = dishes_to_select

    current_order = Order.objects.filter(table_id=table_id, fullfilled=False).first()

    form = OrderItemForm(user=user)
    if request.POST:
        current_order, item = update_order(current_order)
        send_changes(item, user, current_order, table)

    context["current_order"] = current_order



    return render(request, 'waiters/new_order.html', context)