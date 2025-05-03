from django.shortcuts import render

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


# Create your views here.



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
            cart.clear()
            return render(request, 'orders/created_order.html', {'order': order})
    else:
        form = OrderCreateForm(request=request)
        return render(request,'orders/create_order.html', {'form': form})
    